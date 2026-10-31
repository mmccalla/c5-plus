/**
 * Load index.html's inline viewer script in Node and run isolate / path ops.
 * D3 paint is stubbed; filtered() is the isolate contract.
 */
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const HTML_PATH = path.join(ROOT, "index.html");
const GRAPH_PATH = path.join(
  ROOT,
  "c5_enterprise_architecture_knowledge_graph_v5_causal_temporal.json",
);

function extractViewerScript(html) {
  const marker = "<script>\nconst BUILD=";
  const start = html.indexOf(marker);
  if (start < 0) throw new Error("viewer script not found");
  const bodyStart = start + "<script>\n".length;
  const end = html.indexOf("\n</script>", bodyStart);
  if (end < 0) throw new Error("viewer script end not found");
  let code = html.slice(bodyStart, end);
  code = code.replace(/\nsetupAsk\(\);\nsetupLearnFlow\(\);\nboot\(\);/, "\n");
  code = code.replace("const relColours=", "var relColours=");
  code = code.replace(
    "let originalData, ontology, familyColours, selectedClasses, selectedFamilies;",
    "var originalData, ontology, familyColours, selectedClasses, selectedFamilies;",
  );
  code = code.replace(
    'let currentView="Knowledge Graph", focus="business capability", depth=1, highlightedEdges=new Set(), highlightedNodes=new Set();',
    'var currentView="Knowledge Graph", focus="business capability", depth=1, highlightedEdges=new Set(), highlightedNodes=new Set();',
  );
  code = code.replace(
    "let restrictToHighlight=false, depthBeforePath=1, walkExtras=[];",
    "var restrictToHighlight=false, depthBeforePath=1, walkExtras=[];",
  );
  code = code.replace(
    "let svg, layer, linkLayer, labelLayer, nodeLayer, zoom, sim, width, height;",
    "var svg, layer, linkLayer, labelLayer, nodeLayer, zoom, sim, width, height;",
  );
  return code;
}

function makeEl(id) {
  const needsOptions = /Select$|^path(Source|Target)$|^viewSelect$/.test(id);
  return {
    id,
    value: id === "domainFilter" || id === "typeFilter" ? "all" : "",
    checked: true,
    hidden: true,
    innerHTML: "",
    textContent: "",
    style: {},
    options: needsOptions ? [{ value: "x" }] : [],
    classList: { toggle() {}, add() {}, remove() {} },
    dataset: { depth: "1" },
    addEventListener() {},
    appendChild() {},
    add() {},
    onclick: null,
    onchange: null,
    oninput: null,
  };
}

function loadViewer() {
  const html = fs.readFileSync(HTML_PATH, "utf8");
  const graph = JSON.parse(fs.readFileSync(GRAPH_PATH, "utf8"));
  const els = new Map();
  const document = {
    getElementById(id) {
      if (!els.has(id)) els.set(id, makeEl(id));
      return els.get(id);
    },
    querySelector() {
      return makeEl("q");
    },
    querySelectorAll() {
      return [];
    },
    createElement() {
      return makeEl("created");
    },
  };
  const ctx = vm.createContext({
    document,
    console,
    Set,
    Map,
    JSON,
    Array,
    Object,
    Number,
    String,
    Boolean,
    Math,
    Error,
    parseInt,
    parseFloat,
    isNaN,
    Infinity,
    undefined,
    NaN,
    Option: function Option(text, value) {
      this.text = text;
      this.value = value;
    },
    requestAnimationFrame(fn) {
      fn();
    },
    sessionStorage: { getItem() { return null; }, setItem() {}, removeItem() {} },
    location: { protocol: "http:" },
    d3: {},
  });
  vm.runInContext(extractViewerScript(html), ctx);
  ctx.originalData = graph;
  ctx.ontology = graph.relationshipOntology;
  ctx.familyColours = Object.fromEntries(
    Object.entries(graph.relationshipOntology).map(([k, v]) => [k, v.colour]),
  );
  ctx.selectedClasses = new Set(Object.keys(ctx.relColours));
  ctx.selectedFamilies = new Set(Object.keys(graph.relationshipOntology));
  ctx.render = function render() {
    const data = ctx.filtered();
    ctx.__lastFiltered = data;
    const emptyEl = document.getElementById("emptyGraph");
    if (emptyEl) emptyEl.hidden = data.links.length !== 0;
    const sn = document.getElementById("sn");
    if (sn) sn.textContent = String(data.nodes.length);
    const se = document.getElementById("se");
    if (se) se.textContent = String(data.links.length);
  };
  return ctx;
}

function edgeTriple(ctx, edge) {
  return `${ctx.sourceId(edge)}|${edge.label}|${ctx.targetId(edge)}`;
}

function snapshot(ctx) {
  const data = ctx.filtered();
  return {
    nodeIds: data.nodes.map((n) => n.id).sort(),
    edges: data.links.map((e) => edgeTriple(ctx, e)).sort(),
    restrictToHighlight: ctx.restrictToHighlight,
    pathHtml: documentHtml(ctx, "pathResult"),
    emptyHidden: ctx.document.getElementById("emptyGraph").hidden,
    focus: ctx.focus,
    pathSource: ctx.document.getElementById("pathSource").value,
    pathTarget: ctx.document.getElementById("pathTarget").value,
    learnFindingHidden: ctx.document.getElementById("learnFinding").hidden,
    learnErrorHidden: ctx.document.getElementById("learnError").hidden,
  };
}

function documentHtml(ctx, id) {
  return ctx.document.getElementById(id).innerHTML;
}

function setFocus(ctx, nodeId) {
  ctx.focus = nodeId;
  ctx.document.getElementById("focusSelect").value = nodeId;
}

function runOp(ctx, op) {
  if (op.op === "shortest") {
    const path = ctx.findShortestPath(op.src, op.tgt);
    ctx.document.getElementById("pathSource").value = op.src;
    ctx.document.getElementById("pathTarget").value = op.tgt;
    setFocus(ctx, op.src);
    ctx.showPath(path, "Shortest path");
    return {
      found: path !== null,
      nodes: path ? path.nodes : null,
      labels: path ? path.edges.map((e) => e.label) : null,
      isolate: snapshot(ctx),
    };
  }
  if (op.op === "impact") {
    const blast = ctx.findImpactBlast(op.src);
    setFocus(ctx, op.src);
    ctx.document.getElementById("pathSource").value = op.src;
    ctx.showWalk(ctx.hopsFromEdges(blast.edges), "Impact blast");
    return {
      nodes: [...blast.nodes].sort(),
      labels: blast.edges.map((e) => e.label).sort(),
      isolate: snapshot(ctx),
    };
  }
  if (op.op === "showWalk") {
    if (op.focus) setFocus(ctx, op.focus);
    ctx.showWalk(op.hops, op.title || "Walk", op.emptyDetail);
    return { isolate: snapshot(ctx) };
  }
  if (op.op === "learnQ6") {
    ctx.runLearnQ6();
    return { isolate: snapshot(ctx) };
  }
  if (op.op === "filtered") {
    return { isolate: snapshot(ctx) };
  }
  throw new Error(`unknown op: ${op.op}`);
}

const raw = fs.readFileSync(0, "utf8").trim();
const op = JSON.parse(raw || '{"op":"filtered"}');
const ctx = loadViewer();
process.stdout.write(`${JSON.stringify(runOp(ctx, op))}\n`);
