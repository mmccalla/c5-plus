# C5 Enterprise Architecture Knowledge Graph

Interactive v5.3 viewer for the C5 enterprise architecture knowledge graph (226 concepts, 414 relationships).

## Open the graph

Public site, no local server required:

[https://mmccalla.github.io/c5-plus/](https://mmccalla.github.io/c5-plus/)

The same pattern as the [Data Landscape knowledge model](https://mmccalla.github.io/data-landscape-knowledge-model/).

## Run locally

```bash
python3 serve_graph.py
```

Then open [http://127.0.0.1:8765/](http://127.0.0.1:8765/).

## Repository contents

| Path | Role |
|------|------|
| `index.html` | Viewer |
| `c5_enterprise_architecture_knowledge_graph_v5_causal_temporal.json` | Graph source |
| `vendor/d3.v7.min.js` | Local D3 v7 |
| `favicon.svg`, `favicon.ico`, `apple-touch-icon.png` | Site icons |
| `serve_graph.py` | Optional local HTTP server |
| `test_graph_viewer_production.py` | Viewer packaging tests |

Edit the JSON and refresh the page. Export buttons write `c5-enterprise-architecture-knowledge-graph-v5.3.{json,graphml,svg}`.

## Development

```bash
python3 -m pip install -r requirements-dev.txt
pre-commit install
pre-commit run --all-files
python3 -m unittest test_graph_viewer_production.py -v
```

CI runs the same pre-commit hooks and tests on `main` and pull requests. A Pages workflow publishes the static viewer on each push to `main`.

## Licence

MIT. See [LICENSE](LICENSE).
