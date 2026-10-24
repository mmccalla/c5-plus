# Question traversals

This file records directed patterns for the shopfront questions. The graph is a concept projection (metamodel), not a populated client estate. Inspecting it does not require a graph database.

Each edge is stored once, in its primary direction. A hop written with an inverse label (for example `--depended on by→`, the inverse of `consumes`) walks a stored edge backwards. The inverse is declared in `relationCatalogue` in the JSON, not stored as a second edge. `scripts/validate_graph.py` checks that every hop below is either a stored edge or a declared inverse of one.

## Q1 — What depends on this?
**Pattern:** `data product --depended on by→ application component`
**Notes:** The stored edge is `application component --consumes→ data product`. Also `data product --can be affected by→ application change`.

## Q2 — What will this change impact?
**Pattern:** `application change --can affect→ application component --realises→ application service --realises→ business service` ; `application change --can cause→ customer impact --can affect→ outcome`
**Notes:** The viewer's Impact path from `application change` returns these walks. Realisation propagates change upwards: a change to the component impacts the service it realises.

## Q3 — Who owns this?
**Pattern:** `data product --owned by→ stream-aligned team`
**Notes:** Also `data product --accountable steward→ data stewardship`.

## Q4 — Which policies apply?
**Pattern:** `data product --uses→ data object --governed by→ data policy --is type of→ policy --enforced by→ control`
**Notes:** Directed policy chain from the data the product uses, through the policy type, to the enforcing control.

## Q5 — Which customer outcomes are affected?
**Pattern:** `business capability --used by→ value stream stage --part of→ value stream --achieves→ outcome`
**Notes:** Capability to outcome via the value-stream stage that uses it.

## Q6 — What data is involved?
**Pattern:** `application component --consumes→ data product --uses→ data object`
**Notes:** Locked demo. Do not use `application component --manages→ data object` as the Q6 story.

## Q7 — Which teams must be involved?
**Pattern:** `data product --owned by→ stream-aligned team`
**Notes:** Ownership hop from the product to the stream-aligned team.

## Q8 — What feeds this ML model?
**Pattern:** `data product --feeds→ model training pipeline --produces→ ml model`
**Notes:** Product to model via the training pipeline, not a direct product-to-model hop.

## Q9 — Is this data product AI-ready?
**Pattern:** `data product --restricted by→ entitlement` ; `data product --accountable steward→ data stewardship` ; `data product --has lineage→ data lineage` ; `data product --uses→ data object --governed by→ data policy` ; `data product --owned by→ stream-aligned team --implements→ data quality management`
**Notes:** Facets within two hops: access, stewardship, lineage, policy and quality. Facets only — not a readiness certificate.

## Q10 — What lineage exists for X?
**Pattern:** `data product --has lineage→ data lineage`
**Notes:** Direct lineage hop from the product.

## Q11 — Which risks does this control mitigate?
**Pattern:** `control --mitigates→ risk` ; `control --mitigates→ risk exposure`
**Notes:** Both mitigation targets are present in the live JSON.

## Q12 — What fails if this SLO breaks?
**Pattern:** `slo --can affect→ outcome` ; `slo --can affect→ kpi`
**Notes:** Causal `can affect` from the SLO to outcome and KPI.

## Q13 — Who must act on this incident?
**Pattern:** `incident --breaches→ slo --informs→ product team` ; `incident --assigned to→ sre --supports→ stream-aligned team`
**Notes:** The first walk informs the product team via the breached SLO; the second assigns the incident to SRE, who support the stream-aligned team.

## Q14 — What does this capability need from the platform?
**Pattern:** `business capability --exposed via→ business service --realised by→ application service --realised by→ application component --uses→ infrastructure service`
**Notes:** Capability to infrastructure service via the realisation and usage chain in the live JSON.

## Q15 — Which domains or bounded contexts touch this product?
**Pattern:** `data product --owned by→ stream-aligned team --owns→ bounded context`
**Notes:** Ownership-mediated: the product does not link to the bounded context directly; the stream-aligned team owns both.

## Q16 — What retention or PII constraints bind this object?
**Pattern:** `data object --governed by→ data retention and archiving`
**Notes:** Also present: `data object --governed by→ data policy`; `data object --restricted by→ entitlement`; `data object --restricted by→ data sovereignty and residency`.

## Q17 — What customer outcome moves if this KPI moves?
**Pattern:** `kpi --monitors→ outcome`
**Notes:** Direct monitor hop from KPI to outcome.

## Q18 — What is the root cause of this customer impact?
**Pattern:** `root cause --causes→ incident --can cause→ customer impact`
**Notes:** Causal path from `root cause` to `customer impact`. Every Causal edge points from cause to effect, so reading a causal path backwards is root-cause analysis.
