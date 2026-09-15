# C5 Enterprise Architecture Knowledge Graph

Interactive **v5.3** viewer for a directed enterprise-architecture concept graph (226 concepts, 438 relationships). Bidirectional pairs bow apart so the two arrows do not stack. Use it to inspect structure, behaviour, causality, time, governance and semantics, and to walk directed paths between concepts.

## Use the graph

Open the published site: [https://mmccalla.github.io/c5-plus/](https://mmccalla.github.io/c5-plus/)

The page is standalone. You do not need a local server or extra services. It follows the same pattern as the [Data Landscape knowledge model](https://mmccalla.github.io/data-landscape-knowledge-model/).

On the site you can:

- Focus a concept and expand 1–3 hops or the full graph
- Filter by relationship family, class, domain and type
- Run directed path queries (impact, ownership, policy, teams)
- Export `c5-enterprise-architecture-knowledge-graph-v5.3.{json,graphml,svg}`

## Repository

These are the files GitHub serves and deploys. Local scratch files are not listed here.

| Path | Role |
|------|------|
| [index.html](index.html) | Viewer |
| [c5_enterprise_architecture_knowledge_graph_v5_causal_temporal.json](c5_enterprise_architecture_knowledge_graph_v5_causal_temporal.json) | Graph source |
| [vendor/d3.v7.min.js](vendor/d3.v7.min.js) | Vendored D3 v7 |
| [favicon.svg](favicon.svg), [favicon.ico](favicon.ico), [apple-touch-icon.png](apple-touch-icon.png) | Site icons |
| [ontology/README.md](ontology/README.md) | Note on local ontology working copies (gitignored; not published) |
| [requirements-dev.txt](requirements-dev.txt) | Dev dependency: pre-commit |
| [.github/workflows/ci.yml](.github/workflows/ci.yml) | Pre-commit on `main` and pull requests |
| [.github/workflows/pages.yml](.github/workflows/pages.yml) | Publish the static viewer to GitHub Pages |
| [LICENSE](LICENSE) | MIT |

Edit the JSON or viewer, push to `main`, and GitHub Pages republishes the site.

## Development

Quality checks on GitHub are pre-commit only.

```bash
python3 -m pip install -r requirements-dev.txt
pre-commit install
pre-commit run --all-files
```

## Help

Open an issue on this repository.

## Licence

MIT. See [LICENSE](LICENSE).
