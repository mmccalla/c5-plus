#!/usr/bin/env node
// Checks the viewer's question answers against the agreed expected answers in tests/expected-answers.json.
// It runs questions.js, the same code the page uses, on the graph JSON.
//   exact:    the main answer must be exactly the expected elements
//   includes: the main answer must contain at least the expected elements
// It also checks that every question declares a scope matching the agreed one, and that every scoped
// element exists and is an enterprise element.
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const graph = JSON.parse(fs.readFileSync(path.join(root, "c5_enterprise_architecture_knowledge_graph_v5_causal_temporal.json"), "utf8"));
const agreed = JSON.parse(fs.readFileSync(path.join(root, "tests", "expected-answers.json"), "utf8"));
const engine = require(path.join(root, "questions.js"));
engine.loadQuestionGraph(graph);

const problems = [];
const plane = Object.fromEntries(graph.nodes.map((n) => [n.id, n.plane]));
const byId = Object.fromEntries(engine.QUESTIONS.map((q) => [q.id, q]));

for (const [qid, scope] of Object.entries(agreed.scopes)) {
  const q = byId[qid];
  if (!q) {
    problems.push(`${qid}: agreed scope for a question the viewer does not have`);
    continue;
  }
  const declared = [...(q.scope || [])].sort().join("|");
  if (declared !== [...scope.elements].sort().join("|")) problems.push(`${qid}: scope in questions.js differs from tests/expected-answers.json`);
  if (q.about !== scope.about) problems.push(`${qid}: 'about' in questions.js differs from tests/expected-answers.json`);
  for (const el of scope.elements) {
    if (plane[el] !== "enterprise") problems.push(`${qid}: scoped element '${el}' is not an enterprise element`);
  }
}
for (const q of engine.QUESTIONS) {
  if (!agreed.scopes[q.id]) problems.push(`${q.id}: no agreed scope`);
  else if (!(q.scope || []).includes(q.example)) problems.push(`${q.id}: its example '${q.example}' is outside its scope`);
}

let checked = 0;
for (const [qid, spec] of Object.entries(agreed.expected)) {
  const q = byId[qid];
  for (const [el, { answer }] of Object.entries(spec.answers)) {
    checked += 1;
    const got = new Set((q.facets || [q]).flatMap((f) => engine.runQuery(el, f).map((a) => a.id)));
    const missing = answer.filter((x) => !got.has(x));
    const extra = spec.mode === "exact" ? [...got].filter((x) => !answer.includes(x)).sort() : [];
    if (missing.length || extra.length) {
      const parts = [];
      if (missing.length) parts.push(`missing ${missing.join(", ")}`);
      if (extra.length) parts.push(`unexpected ${extra.join(", ")}`);
      problems.push(`${qid} on '${el}': ${parts.join("; ")}`);
    }
  }
}

for (const p of problems) console.log(p);
if (problems.length) {
  console.log(`${problems.length} problem(s) in ${checked} expected answers`);
  process.exit(1);
}
console.log(`questions OK: ${checked} expected answers match, scopes agree for ${Object.keys(agreed.scopes).length} questions`);
