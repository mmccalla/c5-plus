# Which data does this application depend on?

Enterprise and data architects still answer impact, ownership and data-scope questions with slide stacks.
This repo projects those questions as directed traversals over a shared concept model.
It is for EA and data-architecture decisions: impact, productisation, and joining applications to data without a modelling-ticket backlog.

**Live graph:** https://mmccalla.github.io/c5-plus/

**Finding:** From an application component you can reach the data product it consumes and the data object underneath — one directed path instead of three slide layers.

Core questions this model is built to answer:

1. What depends on this?
2. What will this change impact?
3. Who owns this?
4. Which policies apply?
5. Which customer outcomes are affected?
6. What data is involved?
7. Which teams must be involved?

This is a concept projection (metamodel), not a populated client estate, and no graph database is required to inspect it.

How the questions walk (directed patterns, including inverses): [docs/question-traversals.md](docs/question-traversals.md)

## Relationship model

Every relation label is defined once in `relationCatalogue` in the graph JSON. Each entry gives the label's family, class, definition, whether it is transitive, which way a change propagates (`impact`), and its inverse label. Every edge takes these values from its label.

| Family | Classes | Meaning |
|--------|---------|---------|
| Structural | decomposition, classification | What a thing is made of, or what kind of thing it is |
| Behavioural | dependency, flow, activity | Who depends on whom, what flows where, who does what |
| Causal | propagation, mitigation, enablement | Cause and effect; every edge points from cause to effect |
| Temporal | sequence, lifecycle, versioning, validity | Order and validity in time |
| Governance | governance, ownership, measurement | Rules, accountability and measurement |
| Semantic | realisation, representation, alignment | What realises, represents or aligns with what |

Each edge is stored once, in its primary direction. Inverse labels such as `depended on by` are derived from the catalogue, not stored as second edges.

## Using the viewer

The page has two modes. Both share one **Element** search box, which searches all elements; clicking a node selects it.

- **Ask a question** (default): pick one of the 18 questions. It answers for the chosen element, using only the relationships that answer that question. Each answer shows the relationships it rests on, as plain sentences with their definitions. Answers are recorded elements; practices the question reaches are listed under *Practices involved*, and connections that only exist through a practice under *Found only through a practice* (see [docs/planes.md](docs/planes.md)). Each question has an example element you can switch to with one click.
- **Explore**: browse an element's neighbourhood (1–3 steps in either direction, or the whole model) and find a route to a second element. Under **Follow**, a route can use:
  - any relationship in its direction, walking backwards only through declared inverses
  - how a change ripples out (each relation's `impact`)
  - cause → effect only
  - earlier → later only
  - realisation, meaning and structure only

  **Refine** narrows the neighbourhood and routes by family, domain and element type, and always keeps the chosen element. Relationship-class filters sit in a collapsed panel inside Refine. Active refinements are shown under the graph, with a one-click clear.

## Repository

These are the files GitHub serves and deploys. Local scratch files are not listed here.

| Path | Role |
|------|------|
| [index.html](index.html) | Viewer |
| [c5_enterprise_architecture_knowledge_graph_v5_causal_temporal.json](c5_enterprise_architecture_knowledge_graph_v5_causal_temporal.json) | Graph source |
| [vendor/d3.v7.min.js](vendor/d3.v7.min.js) | Vendored D3 v7 |
| [favicon.svg](favicon.svg), [favicon.ico](favicon.ico), [apple-touch-icon.png](apple-touch-icon.png) | Site icons |
| [docs/question-traversals.md](docs/question-traversals.md) | directed question patterns |
| [ontology/README.md](ontology/README.md) | Note on local ontology working copies (gitignored; not published) |
| [scripts/validate_graph.py](scripts/validate_graph.py) | Checks the graph against the relation catalogue and the traversals doc (run by pre-commit) |
| [requirements-dev.txt](requirements-dev.txt) | Dev dependency: pre-commit |
| [.github/workflows/ci.yml](.github/workflows/ci.yml) | Pre-commit on `main` and pull requests |
| [.github/workflows/pages.yml](.github/workflows/pages.yml) | Publish the static viewer to GitHub Pages |
| [LICENSE](LICENSE) | MIT |

Edit the JSON or viewer, push to `main`, and GitHub Pages republishes the site.

## Development

Quality checks on GitHub are pre-commit only. The `validate-graph` hook fails if:

- an edge disagrees with its label's catalogue entry
- an inverse is stored as an edge
- a node has a placeholder description
- the versions in the JSON and `index.html` differ
- a pattern in `docs/question-traversals.md` does not walk real edges
- Structural (part-whole or subtype) edges form a loop. Temporal loops are allowed, because they model recurring lifecycles.
- a concept has no valid plane (enterprise, method or attribute), an attribute is the source of a relationship, a subtype is on a different plane from its parent, or a documented example about an enterprise element passes through a practice. See [docs/planes.md](docs/planes.md).

```bash
python3 -m pip install -r requirements-dev.txt
pre-commit install
pre-commit run --all-files
```

## Help

Open an issue on this repository.

## Licence

MIT. See [LICENSE](LICENSE).
