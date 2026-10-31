# Planes: enterprise, method and attribute

Every concept in the model sits on one of three planes. The plane says whether you would expect to find many of it in a real organisation's records.

| Plane | Concepts | What it holds | Examples |
|---|---|---|---|
| Enterprise | 151 | Things an organisation has many of, each owned and recorded somewhere | application component, container, data product, policy, incident, team |
| Method | 69 | Practices, techniques and patterns: the same in every organisation | data governance, logical data modelling, RBAC, discovery |
| Attribute | 6 | Values that describe an enterprise element rather than things in their own right | a risk's probability, a policy version's effective date |

## The rules

1. **A question about an enterprise element answers with enterprise elements, and never reaches them through a practice.** If a data catalog changes, the model no longer claims initiatives are affected just because the discovery practice uses catalogs and proposes initiatives. In a real estate there is no single "discovery" to pass through.
2. **An attribute is only ever the target of a relationship.** A risk has a probability; a probability does not do anything.
3. **A concept and its subtypes are on the same plane.** A kind of practice is a practice; a kind of team is a team.

Relationships between a practice and an enterprise element keep their ordinary wording, for example *data security policy mandates data encryption* or *product team performs discovery*. They are useful for reading and for questions asked about a practice. They just aren't walked through when the question is about an enterprise element.

The validator checks rules 2 and 3 and every concept's plane. The viewer applies rule 1, and the validator checks that no documented question example breaks it.

## What changed in v5.6.0

- Every concept is tagged with its plane, shown in the viewer's element details.
- One relationship broke rule 3 and was reworded: *data stewardship in cloud is type of data stewardship* became **data stewardship performs data stewardship in cloud**. The first is a practice and the second is the steward role, so one can't be a kind of the other.
- Q9's quality facet is now shown by *data quality monitoring measures data product* (a monitor that exists in the estate) instead of through the data quality management practice.

### Effect on answers (measured)

All 18 questions were run on every element before and after. For questions about enterprise elements, 88 answer items disappear and none are added. Every one of the 88 had been reached only by passing through a practice. Practices also stop being listed as if they were enterprise answers (262 items), for example *database recovery* as something that depends on an infrastructure service. Questions asked about a practice are unchanged except one: Q4 on *data stewardship in cloud* no longer lists the steward role as a policy, an error that came from the reworded subtype relationship.

## Please confirm

### 1. Concepts moved from my first draft

These have real instances in an estate, or are really practices, so they sit on a different plane from where I first put them.

| Concept | Plane | Why |
|---|---|---|
| data quality monitoring | enterprise | Monitors and checks are deployed, owned and alert; an estate has many. |
| model performance monitoring | enterprise | Each deployed model has monitors that detect drift and raise incidents. |
| model experimentation | enterprise | Experiment runs are recorded (for example in an experiment tracker) and produce candidate models. |
| pipeline pattern | enterprise | Golden-path pipeline templates are platform products: provided by a platform team, versioned, used by many pipelines. |
| aggregate | enterprise | Domain-model element: a domain model holds many named aggregates. |
| entity | enterprise | Domain-model element. |
| value object | enterprise | Domain-model element. |
| repository | enterprise | Domain-model element. |
| domain service | enterprise | Domain-model element. |
| data classification | method | Described as the labelling practice; the classification scheme itself is a value on data objects. |
| model governance | method | An oversight practice, parallel to data governance, not a recorded thing. |

### 2. Concepts that are both a practice and a team or role

Each is kept as the team or role, so it can own things and be accountable.

| Concept | Kept as |
|---|---|
| sre | the SRE team |
| data stewardship | the steward role |
| data governance organisation | the councils and forums that hold decision rights |
| product trio | the team of product manager, designer and tech lead |
