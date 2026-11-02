# Question validation: draft for review

Two drafts for you to correct. **Step 1** says which elements each question is about. **Step 2** says what the right answer is for each of those elements, for the five focus questions, and compares it with what the live site (v5.6.0) answers today.

The expected answers are my draft from general enterprise-architecture practice, written before comparing with the model. They are a starting point: where you disagree with an expected answer, mark it, and your answer becomes the test.

## Summary

| Question | Elements in scope | Model matches | Model misses something | Model adds something unexpected |
|---|---|---|---|---|
| Q3 Who owns this? | 58 | 10 | 48 | 0 |
| Q1 What depends on this? | 24 | 11 | 13 | not judged |
| Q2 What will a change to this impact? | 15 | 10 | 5 | not judged |
| Q7 Which teams must be involved? | 10 | 1 | 4 | 5 |
| Q13 Who must act on this incident? | 5 | 1 | 4 | 0 |

- **Q3 is accurate but incomplete.** All 48 of its misses are *no owner found*; it never names the wrong owner. Most in-scope elements have no ownership relationship in the model at all, for example policies, controls, risks, SLOs, ML models and every business element.
- **Q1 and Q2:** the expected answers are *must include* lists. Other items in the model's answer are shown for you to judge, not counted as errors.
- **Q7 and Q13:** several ⚠ rows are arguably right, for example SRE being involved in changes to production components. I have left my narrower expectation so you can decide.

## Step 1: what each question is about

Today every question accepts all 151 enterprise elements. Proposed: each question declares the elements it is about. Asked about anything else, the page would say so (for example *"This question is about controls; data object is a data element"*) and still let you ask anyway, so nobody is blocked.

| Question | About | Elements in scope |
|---|---|---|
| Q3 Who owns this? | Things that should have an accountable owner | 58: api management, apm, application component, application interface, application service, architecture standards, automated retraining pipeline, bounded context, business capability, business glossary, business process, business service, cloud data governance policies, compensating control, component, container, control, data access policies, data catalog, data object, data policies and standards, data policy, data product, data quality monitoring, data quality rules for cloud, data retention and archiving, data security policy, device, enterprise data model, error budget, external system, feature store, infrastructure service, initiative, key result, kpi, master data, ml model, model performance monitoring, model registry, model training pipeline, node, okr, pipeline pattern, policy, procedure, product strategy, products and services, reference data, risk, siem, sli, slo, soar, software system, standard, technology interface, value stream |
| Q1 What depends on this? | Things other things rely on | 24: application component, application service, application interface, software system, container, component, infrastructure service, node, device, technology interface, api management, data product, data object, master data, reference data, data catalog, feature store, ml model, model registry, identity, entitlement, business service, business capability, external system |
| Q2 What will a change to this impact? | Changes, and the things a change is made to | 15: application change, change, change request, deployment, release, application component, application service, application interface, data product, data object, infrastructure service, policy, standard, control, ml model |
| Q7 Which teams must be involved? | Changes, and the things a change is made to | 10: application change, application component, application service, change request, data object, data product, deployment, infrastructure service, ml model, release |
| Q13 Who must act on this incident? | Incidents and failures | 5: incident, model bias, model drift, platform failure, service degradation |
| Q4 Which policies and controls apply? | Things policies and controls apply to | 11: data product, data object, master data, reference data, application interface, application component, infrastructure service, entitlement, products and services, change, ml model |
| Q5 Which customer outcomes are affected? | Business and service elements on the path to customer value | 9: business capability, business service, business process, value stream, value stream stage, application service, products and services, initiative, slo |
| Q6 Which data does this depend on? | Things that use data | 7: application component, application service, software system, ml model, model training pipeline, business process, business capability |
| Q8 What feeds this? | Models, pipelines and the data that feeds them | 7: ml model, candidate model, model version, model training pipeline, automated retraining pipeline, feature store, data product |
| Q9 Is this data product AI-ready? | Data products | 1: data product |
| Q10 What lineage exists for this? | Data | 5: data product, data object, master data, reference data, feature store |
| Q11 Which risks does this control mitigate? | Controls | 3: control, compensating control, mitigation action |
| Q12 What fails if this breaks? | Things that can break | 10: application service, application component, infrastructure service, node, device, slo, data product, ml model, api management, external system |
| Q14 What does this need from the platform? | Business and application elements that run on the platform | 6: business capability, business service, application service, application component, software system, container |
| Q15 Which domains or bounded contexts touch this? | Products, services and data | 5: data product, data object, application service, application component, software system |
| Q16 What retention, privacy or access constraints bind this? | Data that retention, privacy or access rules bind | 5: data object, data product, master data, reference data, feature store |
| Q17 What customer outcome moves if this moves? | Measures | 7: kpi, key result, okr, sli, dora metric, finops metric, measure |
| Q18 What could cause this? | Effects and failures | 7: customer impact, operational impact, regulatory impact, incident, service degradation, platform failure, model drift |

That is 195 question–element pairs in scope, instead of 2718.

## Step 2: expected answers for the five focus questions

Verdict key: ✓ the model gives the expected answer · ✗ the model misses something · ⚠ the model also gives something not expected.

### Q3 Who owns this?

| Element | Expected | Model answers now | Verdict | Why this is expected |
|---|---|---|---|---|
| api management | platform team | — | ✗ misses platform team | A platform product. |
| apm | platform team | — | ✗ misses platform team | Shared operational tooling. |
| application component | stream-aligned team | stream-aligned team | ✓ | The delivery team that builds and runs it. |
| application interface | stream-aligned team | — | ✗ misses stream-aligned team | Owned with the service it exposes. |
| application service | stream-aligned team | stream-aligned team | ✓ | The delivery team that runs it. |
| architecture standards | business role | — | ✗ misses business role | A named owner, such as a chief architect. |
| automated retraining pipeline | stream-aligned team | — | ✗ misses stream-aligned team | Owned with the model. |
| bounded context | stream-aligned team | stream-aligned team | ✓ | One team per bounded context. |
| business capability | business role | — | ✗ misses business role | A business leader owns each capability. |
| business glossary | data governance organisation | — | ✗ misses data governance organisation | Owned by data governance. |
| business process | business role | — | ✗ misses business role | A process owner. |
| business service | business role | — | ✗ misses business role | A business service owner. |
| cloud data governance policies | data governance organisation | — | ✗ misses data governance organisation | Data governance. |
| compensating control | business role | — | ✗ misses business role | A named control owner. |
| component | complicated-subsystem team, stream-aligned team | complicated-subsystem team, stream-aligned team | ✓ | Usually the delivery team; specialist subsystems belong to a complicated-subsystem team. |
| container | stream-aligned team | stream-aligned team | ✓ | Owned with its software system. |
| control | business role | — | ✗ misses business role | A named control owner. |
| data access policies | data governance organisation | — | ✗ misses data governance organisation | Data governance. |
| data catalog | platform team | — | ✗ misses platform team | A platform product. |
| data object | data stewardship, stream-aligned team | — | ✗ misses data stewardship, stream-aligned team | Through the data product that holds it. |
| data policies and standards | data governance organisation | — | ✗ misses data governance organisation | Data governance. |
| data policy | data governance organisation | — | ✗ misses data governance organisation | Data policies are owned by data governance. |
| data product | data stewardship, stream-aligned team | data stewardship, stream-aligned team | ✓ | Owned by its domain team; a steward is accountable for the data. |
| data quality monitoring | stream-aligned team | — | ✗ misses stream-aligned team | Owned by the team of the data product it watches. |
| data quality rules for cloud | data governance organisation | — | ✗ misses data governance organisation | Data governance. |
| data retention and archiving | data governance organisation | — | ✗ misses data governance organisation | Data governance. |
| data security policy | data governance organisation | — | ✗ misses data governance organisation | Data governance. |
| device | platform team | — | ✗ misses platform team | Platform. |
| enterprise data model | data governance organisation | — | ✗ misses data governance organisation | Owned by data governance. |
| error budget | stream-aligned team | — | ✗ misses stream-aligned team | Owned with its SLO. |
| external system | stream-aligned team | — | ✗ misses stream-aligned team | Supplied externally; internally, the team that integrates with it owns the relationship. |
| feature store | platform team | — | ✗ misses platform team | A shared platform product. |
| infrastructure service | platform team | — | ✗ misses platform team | Platform capabilities belong to the platform team. |
| initiative | product team | — | ✗ misses product team | The product team that delivers it. |
| key result | product team | product team | ✓ | Owned with its OKR. |
| kpi | business role | — | ✗ misses business role | A business owner for the measure. |
| master data | data stewardship | — | ✗ misses data stewardship | Master data is stewarded. |
| ml model | stream-aligned team | — | ✗ misses stream-aligned team | The team whose product uses it. |
| model performance monitoring | stream-aligned team | — | ✗ misses stream-aligned team | Owned with the model; SRE may operate it. |
| model registry | platform team | — | ✗ misses platform team | A shared platform product. |
| model training pipeline | stream-aligned team | — | ✗ misses stream-aligned team | Owned with the model. |
| node | platform team | platform team | ✓ | Platform. |
| okr | product team | product team | ✓ | The team accountable for it. |
| pipeline pattern | platform team | — | ✗ misses platform team | Golden-path templates are platform products. |
| policy | business role | — | ✗ misses business role | A named policy owner. |
| procedure | business role | — | ✗ misses business role | A named procedure owner. |
| product strategy | product team | — | ✗ misses product team | The product team. |
| products and services | product team | — | ✗ misses product team | The product team. |
| reference data | data stewardship | — | ✗ misses data stewardship | Reference data is stewarded. |
| risk | business role | — | ✗ misses business role | A named risk owner. |
| siem | platform team | — | ✗ misses platform team | Shared operational tooling. |
| sli | stream-aligned team | — | ✗ misses stream-aligned team | Owned with its SLO. |
| slo | stream-aligned team | — | ✗ misses stream-aligned team | Set and owned by the team that runs the service. |
| soar | platform team | — | ✗ misses platform team | Shared operational tooling. |
| software system | stream-aligned team | stream-aligned team | ✓ | The delivery team that runs it. |
| standard | business role | — | ✗ misses business role | A named standard owner. |
| technology interface | platform team | — | ✗ misses platform team | Platform. |
| value stream | business role | — | ✗ misses business role | A value stream owner. |

### Q1 What depends on this?

| Element | Expected | Model answers now | Verdict | Why this is expected |
|---|---|---|---|---|
| api management | application interface | — | ✗ misses application interface | APIs are published through it. |
| application component | application service | application service (+3 more: business capability, business process, business service) | ✓ | Services are realised by components. |
| application interface | application component | — (+6 more: application service, business capability, business process, business service, customer, products and services) | ✗ misses application component | Callers depend on the interface. |
| application service | application interface, business service | business service (+4 more: business capability, business process, product strategy, value stream stage) | ✗ misses application interface | Business services are realised by it; interfaces expose it. |
| business capability | product strategy, value stream stage | product strategy, value stream stage (+1 more: initiative) | ✓ | Value stream stages and strategy rely on capabilities. |
| business service | business capability, products and services | business capability (+4 more: business process, initiative, product strategy, value stream stage) | ✗ misses products and services | Products implement it; capabilities are exposed through it. |
| component | container | — | ✗ misses container | Containers are made of components. |
| container | application component | application component (+2 more: application service, business service) | ✓ | Components run in containers. |
| data catalog | data object | —<br><small>practices: discovery</small> | ✗ misses data object | Data is registered and found through it. |
| data object | application component, application service, data product | application component, application service, data product (+8 more: business capability, business object, business process, business service, feature store, model training pipeline, product strategy, value stream stage)<br><small>practices: data preparation; only through a practice: 1</small> | ✓ | Products are built from it; applications manage and use it. |
| data product | application component, model training pipeline | application component, model training pipeline (+3 more: application service, business service, feature store)<br><small>practices: data preparation; only through a practice: 1</small> | ✓ | Applications consume it; training pipelines are fed by it. |
| device | infrastructure service | infrastructure service (+4 more: api management, application component, application service, pipeline pattern)<br><small>practices: data encryption (at-rest, in-transit), database recovery, database support</small> | ✓ | Infrastructure runs on devices. |
| entitlement | application interface | — | ✗ misses application interface | Interfaces authorise through entitlements. |
| external system | software system | software system (+5 more: anti-corruption layer, bounded context, business capability, product strategy, value stream stage) | ✓ | Systems that integrate with it. |
| feature store | application component, model training pipeline | application component, model training pipeline (+2 more: application service, business service) | ✓ | Training and inference read features. |
| identity | entitlement | — | ✗ misses entitlement | Entitlements are granted to identities. |
| infrastructure service | api management, application component, pipeline pattern | api management, application component, pipeline pattern (+2 more: application service, business service)<br><small>practices: data encryption (at-rest, in-transit), database recovery, database support</small> | ✓ | Everything that runs on the platform. |
| master data | application component, data product | — | ✗ misses application component, data product | Master data is used across products and applications. |
| ml model | application component | application component (+2 more: application service, business service) | ✓ | Applications call models. |
| model registry | ml model | — | ✗ misses ml model | Models are registered and promoted through it. |
| node | application interface, infrastructure service | application interface (+4 more: application service, business service, customer, products and services) | ✗ misses infrastructure service | Services and interfaces run on nodes. |
| reference data | application component, data product | — | ✗ misses application component, data product | Same as master data. |
| software system | business capability | business capability (+4 more: bounded context, initiative, product strategy, value stream stage) | ✓ | Capabilities are realised by systems. |
| technology interface | application component, infrastructure service | — (+1 more: repository) | ✗ misses application component, infrastructure service | Callers of the platform interface. |

### Q2 What will a change to this impact?

| Element | Expected | Model answers now | Verdict | Why this is expected |
|---|---|---|---|---|
| application change | application component, application service, business service, customer impact, data product, service degradation | application component, application service, business service, customer impact, data product, service degradation (+31 more: business capability, business process, candidate model, customer, customer jobs, data lineage, deployment, dora metric…)<br><small>practices: data preparation, end-to-end data lineage; only through a practice: 1</small> | ✓ | Code and config changes reach components, the services they realise, the data they touch, and can degrade service for customers. |
| application component | application service, business service | application service, business service (+12 more: business capability, business process, customer, customer jobs, data lineage, dora metric, product strategy, products and services…)<br><small>practices: end-to-end data lineage</small> | ✓ | Changing a component changes the services it realises. |
| application interface | application component | — (+13 more: application service, business capability, business process, business service, customer, customer jobs, customer segment, fit hypothesis…) | ✗ misses application component | Callers of the interface. |
| application service | application interface, business service | business service (+12 more: business capability, business process, customer, customer jobs, customer segment, fit hypothesis, initiative, product strategy…) | ✗ misses application interface | Changing a service changes what is exposed and what it realises. |
| change | application component | — (+3 more: change request, deployment, release) | ✗ misses application component | A change is a change to something; at least the components changed. |
| change request | change | — | ✗ misses change | A request leads to a change. |
| control | risk, risk exposure | risk, risk exposure (+30 more: api management, application component, application service, business capability, business object, business process, business service, candidate model…)<br><small>practices: data encryption (at-rest, in-transit), data preparation, database recovery, database support, discovery, end-to-end data lineage</small> | ✓ | Risks the control mitigates. |
| data object | application component, data product | application component, data product (+25 more: application service, business capability, business object, business process, business service, candidate model, customer, customer jobs…)<br><small>practices: data preparation, discovery, end-to-end data lineage; only through a practice: 4</small> | ✓ | Products and applications built on it. |
| data product | application component, ml model, model training pipeline | application component, ml model, model training pipeline (+14 more: application service, business capability, business process, business service, candidate model, data lineage, dora metric, feature store…)<br><small>practices: data preparation, end-to-end data lineage; only through a practice: 1</small> | ✓ | Consumers, and models trained on it. |
| deployment | release | release | ✓ | A deployment leads to a release. |
| infrastructure service | application component, application service | application component, application service (+24 more: api management, bounded context, business capability, business process, business service, candidate model, code element, container…)<br><small>practices: data encryption (at-rest, in-transit), database recovery, database support, end-to-end data lineage</small> | ✓ | Everything running on it. |
| ml model | application component | application component (+11 more: application service, business capability, business process, business service, data lineage, dora metric, model registry, products and services…)<br><small>practices: end-to-end data lineage</small> | ✓ | Applications that call it. |
| policy | application interface, control, data product | application interface, control, data product (+42 more: api management, application component, application service, business capability, business object, business process, business service, candidate model…)<br><small>practices: data encryption (at-rest, in-transit), data preparation, database recovery, database support, end-to-end data lineage; only through a practice: 1</small> | ✓ | Controls that enforce it and what it governs. |
| release | application service | — | ✗ misses application service | A release changes what users get from the service. |
| standard | pipeline pattern | pipeline pattern (+20 more: application component, application service, bounded context, business capability, business process, business service, candidate model, code element…) | ✓ | Patterns that implement the standard. |

### Q7 Which teams must be involved?

| Element | Expected | Model answers now | Verdict | Why this is expected |
|---|---|---|---|---|
| application change | data stewardship, stream-aligned team | data governance organisation, data stewardship, product team, sre, stream-aligned team | ⚠ also data governance organisation, product team, sre | Owners of the changed components and services, and stewards of data products they affect. |
| application component | stream-aligned team | sre, stream-aligned team | ⚠ also sre | Its owner, and owners of what depends on it. |
| application service | stream-aligned team | stream-aligned team | ✓ | Its owner, and owners of what depends on it. |
| change request | stream-aligned team | — | ✗ misses stream-aligned team | The team that owns what is being changed. |
| data object | data stewardship, stream-aligned team | data governance organisation, data stewardship, stream-aligned team | ⚠ also data governance organisation | Through the data products that use it. |
| data product | data stewardship, stream-aligned team | data governance organisation, data stewardship, enabling team, sre, stream-aligned team<br><small>only through a practice: 1</small> | ⚠ also data governance organisation, enabling team, sre | Its owning team and steward, and teams that consume it. |
| deployment | stream-aligned team | — | ✗ misses stream-aligned team | The owning delivery team. |
| infrastructure service | platform team, stream-aligned team | sre, stream-aligned team | ✗ misses platform team ⚠ also sre | The platform team, and teams whose components run on it. |
| ml model | stream-aligned team | sre, stream-aligned team | ⚠ also sre | The owning team, and teams whose applications call it. |
| release | stream-aligned team | — | ✗ misses stream-aligned team | The owning delivery team. |

### Q13 Who must act on this incident?

| Element | Expected | Model answers now | Verdict | Why this is expected |
|---|---|---|---|---|
| incident | product team, sre, stream-aligned team | product team, sre, stream-aligned team | ✓ | SRE runs the response, the service's owning team fixes it, the product team is informed through the breached SLO. |
| model bias | stream-aligned team | — | ✗ misses stream-aligned team | The model's owning team. |
| model drift | sre, stream-aligned team | — | ✗ misses sre, stream-aligned team | The model's owning team retrains; SRE runs the monitoring. |
| platform failure | platform team, sre, stream-aligned team | product team, sre, stream-aligned team | ✗ misses platform team ⚠ also product team | The platform team fixes it, SRE coordinates, and teams whose services run on it act on their side. |
| service degradation | product team, sre, stream-aligned team | product team, stream-aligned team | ✗ misses sre | Same responders as an incident on that service, including the product team informed through the breached SLO. |

## Other questions: answered or not, within their proposed scope

Expected answers for these are not drafted yet. This shows how many in-scope elements get any answer today.

| Question | In scope | Answered | Practices only | Nothing |
|---|---|---|---|---|
| Q4 Which policies and controls apply? | 11 | 9 | 1 | 1 |
| Q5 Which customer outcomes are affected? | 9 | 9 | 0 | 0 |
| Q6 Which data does this depend on? | 7 | 5 | 0 | 2 |
| Q8 What feeds this? | 7 | 6 | 0 | 1 |
| Q9 Is this data product AI-ready? | 1 | 1 | 0 | 0 |
| Q10 What lineage exists for this? | 5 | 2 | 0 | 3 |
| Q11 Which risks does this control mitigate? | 3 | 3 | 0 | 0 |
| Q12 What fails if this breaks? | 10 | 1 | 0 | 9 |
| Q14 What does this need from the platform? | 6 | 4 | 0 | 2 |
| Q15 Which domains or bounded contexts touch this? | 5 | 4 | 0 | 1 |
| Q16 What retention, privacy or access constraints bind this? | 5 | 2 | 2 | 1 |
| Q17 What customer outcome moves if this moves? | 7 | 3 | 0 | 4 |
| Q18 What could cause this? | 7 | 6 | 0 | 1 |

## How to review

- **Step 1:** add or remove elements from any question's scope.
- **Step 2:** for each row, either agree with *Expected* or give the answer you would expect. Start with the ✗ and ⚠ rows, where the model and my draft disagree.
- Once agreed, the expected answers become an automated test, and the ✗ rows become the fix list.
