// The question engine: the 18 questions and the graph walks that answer them.
// Loaded by index.html, and by scripts/check_questions.js so the automated check runs this exact code.
/* eslint-disable no-unused-vars */
let catalogue, nodeById, outEdges, inEdges, typeParents;
function sourceId(e){return typeof e.source==="string"?e.source:e.source.id}
function targetId(e){return typeof e.target==="string"?e.target:e.target.id}

// ---- Questions ---------------------------------------------------------------
// A question walks outward from the element along the relationships that answer it.
// Each rule matches edges by family, class or label, and says which way to walk them:
// "out" follows the stored direction, "in" walks it backwards, "both" either way.
// {impact:true} walks each relation the way a change propagates (relationCatalogue.impact).
const GOV_IN=["governs","applied to","mandates","defines","controls","establishes","authorises"];
const GOV_OUT=["governed by","restricted by","constrained by","enforced by"];
const TEAMS=["stream-aligned team","platform team","enabling team","complicated-subsystem team","product team","product trio","sre","business role","data stewardship","data governance organisation"];
// Teams that act on incidents: operating teams, not business owners or governance bodies.
const OPERATING_TEAMS=["stream-aligned team","platform team","complicated-subsystem team","product team","product trio","sre","data stewardship"];
const OUTCOMES=["outcome","customer impact","customer gains","stakeholder","value item","kpi","key result","okr"];
const QUESTIONS=[
  {id:"Q1",about:"Things other things rely on",scope:["application component", "application service", "application interface", "software system", "container", "component", "infrastructure service", "node", "device", "technology interface", "api management", "data product", "data object", "master data", "reference data", "data catalog", "feature store", "ml model", "model registry", "identity", "entitlement", "business service", "business capability", "external system"],group:"Dependencies and impact",text:"What depends on this?",example:"data product",depth:3,
   rules:[{cls:["dependency"],dir:"in"},{labels:["feeds","input for","authorises","grants"],dir:"out"},{labels:["exposed via"],dir:"both"},{labels:["realised by","realised as","delivered via","registered in"],dir:"in"},
          {labels:["contains","comprises","includes","has","composed of"],dir:"in"},{labels:["is type of"],dir:"out"}],target:{notVia:["is type of"]}},
  {id:"Q2",about:"Changes, and the things a change is made to",scope:["application change", "deployment", "release", "application component", "application service", "application interface", "data product", "data object", "infrastructure service", "policy", "standard", "control", "ml model"],group:"Dependencies and impact",text:"What will a change to this impact?",example:"application change",depth:4,rules:[{impact:true}]},
  {id:"Q5",about:"Business and service elements on the path to customer value",scope:["business capability", "business service", "business process", "value stream", "value stream stage", "application service", "products and services", "initiative", "slo"],group:"Dependencies and impact",text:"Which customer outcomes are affected?",example:"business capability",depth:5,
   rules:[{impact:true},{labels:["part of"],dir:"out"},{labels:["has","contains","comprises","includes"],dir:"in"}],target:{ids:OUTCOMES}},
  {id:"Q12",about:"Things that can break",scope:["application service", "application component", "infrastructure service", "node", "device", "slo", "data product", "ml model", "api management", "external system"],group:"Dependencies and impact",text:"What fails if this breaks?",example:"slo",depth:4,rules:[{fam:["Causal"],dir:"out"}]},
  {id:"Q14",about:"Business and application elements that run on the platform",scope:["business capability", "business service", "application service", "application component", "software system", "container"],group:"Dependencies and impact",text:"What does this need from the platform?",example:"business capability",depth:5,
   rules:[{labels:["realised by","realised as","exposed via","delivered via","implemented by"],dir:"out"},{labels:["implements"],dir:"in"},{cls:["dependency"],dir:"out"}],target:{domains:["platform-infra"]}},
  {id:"Q3",about:"Things that should have an accountable owner",scope:["api management", "apm", "application component", "application interface", "application service", "architecture standards", "automated retraining pipeline", "bounded context", "business capability", "business glossary", "business process", "business service", "cloud data governance policies", "compensating control", "component", "container", "control", "data access policies", "data catalog", "data object", "data policies and standards", "data policy", "data product", "data quality monitoring", "data quality rules for cloud", "data retention and archiving", "data security policy", "device", "enterprise data model", "error budget", "external system", "feature store", "infrastructure service", "initiative", "key result", "kpi", "master data", "ml model", "model performance monitoring", "model registry", "model training pipeline", "node", "okr", "pipeline pattern", "policy", "procedure", "product strategy", "products and services", "reference data", "risk", "siem", "sli", "slo", "soar", "software system", "standard", "technology interface", "value stream"],group:"Ownership and governance",text:"Who owns this?",example:"data product",depth:3,
   // Owned directly, or through what it belongs to: the whole it is part of, what it realises, the product that uses it,
   // the system that integrates with it, the service an SLO measures. Only the nearest owners count.
   rules:[{labels:["owns","accountable for"],dir:"in"},{labels:["part of","measures","produces"],dir:"out"},{labels:["has","contains","comprises","includes"],dir:"in"},
          {labels:["realised by","implemented by","uses","integrates with","targets","defines","exposed via"],dir:"in"}],target:{via:["owns","accountable for"]},nearest:true},
  {id:"Q7",about:"Changes, and the things a change is made to",scope:["application change", "application component", "application service", "data object", "data product", "deployment", "infrastructure service", "ml model", "release"],group:"Ownership and governance",text:"Which teams must be involved?",example:"data product",depth:3,
   // Owners of what the change reaches, and who supports it; teams are answers, never stepping stones.
   rules:[{impact:true},{cls:["ownership"],dir:"in"},{labels:["supports"],dir:"in"}],target:{ids:OPERATING_TEAMS},stopAt:TEAMS},
  {id:"Q4",about:"Things policies and controls apply to",scope:["data product", "data object", "master data", "reference data", "application interface", "application component", "infrastructure service", "entitlement", "products and services", "change", "ml model"],group:"Ownership and governance",text:"Which policies and controls apply?",example:"data product",depth:4,
   rules:[{cls:["dependency"],dir:"out"},{labels:GOV_OUT,dir:"out"},{labels:GOV_IN,dir:"in"},{labels:["is type of"],dir:"out"},{labels:["enforces"],dir:"in"}],target:{viaClass:["governance","classification"]}},
  {id:"Q16",about:"Data that retention, privacy or access rules bind",scope:["data object", "data product", "master data", "reference data", "feature store"],group:"Ownership and governance",text:"What retention, privacy or access constraints bind this?",example:"data object",depth:2,
   rules:[{labels:GOV_OUT,dir:"out"},{labels:GOV_IN,dir:"in"}],target:{viaClass:["governance"]}},
  {id:"Q11",about:"Controls",scope:["control", "compensating control", "mitigation action"],group:"Ownership and governance",text:"Which risks does this control mitigate?",example:"control",depth:2,
   rules:[{cls:["mitigation"],dir:"out"},{labels:["is type of"],dir:"in"}],target:{isA:["risk","risk exposure"]}},
  {id:"Q6",about:"Things that use data",scope:["application component", "application service", "software system", "ml model", "model training pipeline", "business process", "business capability"],group:"Data and lineage",text:"Which data does this depend on?",example:"application component",depth:2,
   rules:[{cls:["dependency","flow"],dir:"out"},{labels:["manages","composed of","realised by"],dir:"out"}],target:{domains:["information-data"]}},
  {id:"Q8",about:"Models, pipelines and the data that feeds them",scope:["ml model", "candidate model", "model version", "model training pipeline", "automated retraining pipeline", "feature store", "data product"],group:"Data and lineage",text:"What feeds this?",example:"ml model",depth:3,
   rules:[{cls:["flow"],dir:"in"},{labels:["deployed as","promotes to"],dir:"in"},{cls:["dependency"],dir:"out"}]},
  {id:"Q10",about:"Data",scope:["data product", "data object", "master data", "reference data", "feature store"],group:"Data and lineage",text:"What lineage exists for this?",example:"data product",depth:2,
   rules:[{labels:["has lineage"],dir:"out"},{labels:["traces","generates"],dir:"in"},{cls:["dependency"],dir:"out"}],target:{match:"lineage"}},
  {id:"Q9",about:"Data products",scope:["data product"],group:"Data and lineage",text:"Is this data product AI-ready?",example:"data product",facets:[
    {name:"Access is controlled",depth:1,rules:[{labels:["restricted by"],dir:"out"}]},
    {name:"Someone is accountable",depth:1,rules:[{labels:["accountable for","owns"],dir:"in"}]},
    {name:"Lineage is recorded",depth:1,rules:[{labels:["has lineage"],dir:"out"},{labels:["traces"],dir:"in"}]},
    {name:"Data policy applies",depth:2,rules:[{cls:["dependency"],dir:"out"},{labels:["governed by"],dir:"out"},{labels:["governs"],dir:"in"}],target:{isA:["data policy","policy"]}},
    {name:"Quality is managed",depth:2,rules:[{labels:["owns"],dir:"in"},{labels:["implements"],dir:"out"},{labels:["measures","monitors"],dir:"in"}],target:{match:"quality"}}]},
  {id:"Q18",about:"Effects and failures",scope:["customer impact", "operational impact", "regulatory impact", "incident", "service degradation", "platform failure", "model drift"],group:"Causes and sequence",text:"What could cause this?",example:"customer impact",depth:4,rules:[{fam:["Causal"],dir:"in"}]},
  {id:"Q13",about:"Incidents and failures",scope:["incident", "model bias", "model drift", "platform failure", "service degradation"],group:"Causes and sequence",text:"Who must act on this incident?",example:"incident",depth:3,
   // The team it is assigned to, the owner and supporters of the affected service, and those the breached SLO informs.
   rules:[{fam:["Causal"],dir:"out"},{labels:["assigned to","informs","measures"],dir:"out"},{cls:["ownership"],dir:"in"},{labels:["supports"],dir:"in"}],target:{ids:OPERATING_TEAMS},stopAt:TEAMS},
  {id:"Q17",about:"Measures",scope:["kpi", "key result", "okr", "sli", "dora metric", "finops metric", "measure"],group:"Causes and sequence",text:"What customer outcome moves if this moves?",example:"kpi",depth:3,
   rules:[{cls:["measurement"],dir:"out"},{fam:["Causal"],dir:"out"},{labels:["informs"],dir:"out"}],target:{ids:OUTCOMES}},
  {id:"Q15",about:"Products, services and data",scope:["data product", "data object", "application service", "application component", "software system"],group:"Causes and sequence",text:"Which domains or bounded contexts touch this?",example:"data product",depth:3,
   rules:[{cls:["ownership"],dir:"in"},{labels:["owns"],dir:"out"},{cls:["realisation"],dir:"both"},{labels:["part of"],dir:"out"}],target:{domains:["ddd"]}},
];
const ROUTES={
  directed:{label:"Any relationship, in its direction",mode:"directed"},
  impact:{label:"How a change ripples out",mode:"impact"},
  causal:{label:"Cause → effect",mode:"forward",families:["Causal"]},
  temporal:{label:"Earlier → later",mode:"forward",families:["Temporal"]},
  semantic:{label:"Realisation, meaning and structure",mode:"directed",families:["Semantic","Structural"]},
};

function relation(e){return catalogue[e.label]||{}}
function indexGraph(data){
  nodeById=new Map(data.nodes.map(n=>[n.id,n])); outEdges=new Map(); inEdges=new Map(); typeParents=new Map();
  data.links.forEach(e=>{
    (outEdges.get(e.source)||outEdges.set(e.source,[]).get(e.source)).push(e);
    (inEdges.get(e.target)||inEdges.set(e.target,[]).get(e.target)).push(e);
    if(e.label==="is type of") (typeParents.get(e.source)||typeParents.set(e.source,[]).get(e.source)).push(e.target);
  });
}
function isA(id,base){const seen=new Set(),stack=[id]; while(stack.length){const n=stack.pop(); if(n===base)return true; if(seen.has(n))continue; seen.add(n); (typeParents.get(n)||[]).forEach(p=>stack.push(p))} return false}

function loadQuestionGraph(data){catalogue=data.relationCatalogue; indexGraph(data)}

// ---- Traversal ------------------------------------------------------------------
// A rule with labels matches those labels; otherwise it matches its classes; fam narrows either.
function ruleMatches(rule,e){
  if(rule.fam&&!rule.fam.includes(e.relationshipFamily))return false;
  if(rule.labels)return rule.labels.includes(e.label);
  if(rule.cls)return rule.cls.includes(e.relationshipClass);
  return true;
}
// Steps out of a node under a set of rules: {to, edge, backward}.
function ruleSteps(id,rules,links){
  const ok=e=>!links||links.has(e), out=[];
  (outEdges.get(id)||[]).filter(ok).forEach(e=>{if(rules.some(r=>r.impact?["forward","both"].includes(relation(e).impact):(r.dir!=="in"&&ruleMatches(r,e))))out.push({to:e.target,edge:e,backward:false})});
  (inEdges.get(id)||[]).filter(ok).forEach(e=>{if(rules.some(r=>r.impact?["reverse","both"].includes(relation(e).impact):(r.dir!=="out"&&ruleMatches(r,e))))out.push({to:e.source,edge:e,backward:true})});
  return out;
}
// Steps for route-finding modes.
function modeSteps(id,mode,families,links){
  const ok=e=>(!links||links.has(e))&&(!families||families.includes(e.relationshipFamily)), out=[];
  (outEdges.get(id)||[]).filter(ok).forEach(e=>{if(mode!=="impact"||["forward","both"].includes(relation(e).impact))out.push({to:e.target,edge:e,backward:false})});
  (inEdges.get(id)||[]).filter(ok).forEach(e=>{const r=relation(e); if((mode==="directed"&&r.inverse)||(mode==="any")||(mode==="impact"&&["reverse","both"].includes(r.impact)))out.push({to:e.source,edge:e,backward:true})});
  return out;
}
function bfs(src,stepsOf,maxDepth=Infinity){
  const prev=new Map([[src,null]]), depth=new Map([[src,0]]), q=[src];
  while(q.length){const u=q.shift(); if(depth.get(u)>=maxDepth)continue; stepsOf(u).forEach(st=>{if(!prev.has(st.to)){prev.set(st.to,{...st,from:u});depth.set(st.to,depth.get(u)+1);q.push(st.to)}})}
  const pathTo=t=>{const steps=[];let c=t;while(prev.get(c)){steps.push(prev.get(c));c=prev.get(c).from}return steps.reverse()};
  return{prev,depth,pathTo};
}
function matchesTarget(target,id,lastStep){
  if(!target)return true;
  const n=nodeById.get(id);
  if(target.ids&&!target.ids.includes(id))return false;
  if(target.domains&&!target.domains.includes(n.domain))return false;
  if(target.isA&&!target.isA.some(b=>isA(id,b)))return false;
  if(target.match&&!id.includes(target.match))return false;
  if(target.via&&!target.via.includes(lastStep.edge.label))return false;
  if(target.viaClass&&!target.viaClass.includes(lastStep.edge.relationshipClass))return false;
  if(target.notVia&&target.notVia.includes(lastStep.edge.label))return false;
  return true;
}
// A question about an enterprise element answers with enterprise elements, and never reaches them
// through a practice (planes.rules in the JSON). Questions about a practice may walk anywhere.
// A question may stop at certain elements, such as teams: it answers with them but does not walk on from them.
function stops(spec,element,id){return id!==element&&!!spec.stopAt&&spec.stopAt.includes(id)}
function runQuery(element,spec){
  const enterprise=nodeById.get(element)?.plane!=="method";
  const r=bfs(element,id=>stops(spec,element,id)?[]:ruleSteps(id,spec.rules).filter(st=>!enterprise||nodeById.get(st.to).plane!=="method"),spec.depth);
  const answers=[];
  r.prev.forEach((st,id)=>{if(st&&matchesTarget(spec.target,id,st))answers.push({id,steps:r.pathTo(id)})});
  answers.sort((a,b)=>a.steps.length-b.steps.length||a.id.localeCompare(b.id));
  return spec.nearest&&answers.length?answers.filter(a=>a.steps.length===answers[0].steps.length):answers;
}
// Everything else the question reaches when practices are not skipped, in two groups:
// practices reached directly, and recorded elements reachable only by passing through a practice.
function classifyQuery(element,spec){
  const direct=runQuery(element,spec);
  if(nodeById.get(element)?.plane==="method")return{direct,practices:[],indirect:[]};
  const seen=new Set(direct.map(a=>a.id)), wide=bfs(element,id=>stops(spec,element,id)?[]:ruleSteps(id,spec.rules),spec.depth), practices=[], indirect=[];
  wide.prev.forEach((st,id)=>{
    if(!st||seen.has(id)||!matchesTarget(spec.target,id,st))return;
    const steps=wide.pathTo(id), throughPractice=steps.slice(0,-1).some(x=>nodeById.get(x.to).plane==="method");
    if(throughPractice)indirect.push({id,steps});
    else if(nodeById.get(id).plane==="method")practices.push({id,steps});
  });
  const order=(a,b)=>a.steps.length-b.steps.length||a.id.localeCompare(b.id);
  return{direct,practices:practices.sort(order),indirect:indirect.sort(order)};
}
function findRoute(src,tgt,route,links){
  let r=bfs(src,id=>modeSteps(id,route.mode,route.families,links)), note="";
  if(!r.prev.has(tgt)&&route.mode==="directed"&&!route.families){r=bfs(src,id=>modeSteps(id,"any",null,links)); note="No route follows the arrows, so this one ignores direction."}
  return r.prev.has(tgt)?{steps:r.pathTo(tgt),note}:null;
}

if(typeof module!=="undefined")module.exports={QUESTIONS,ROUTES,loadQuestionGraph,runQuery,classifyQuery,findRoute,isA,get nodeById(){return nodeById}};
