# C5 Enterprise Architecture Knowledge Graph

Interactive v5.3 viewer for the C5 enterprise architecture knowledge graph (226 concepts, 414 relationships).

## Run the viewer

The page loads the graph from JSON, so it must be served over HTTP:

```bash
python3 serve_graph.py
```

Then open [http://127.0.0.1:8765/c5_enterprise_architecture_knowledge_graph_v5_3_arrows_legend.html](http://127.0.0.1:8765/c5_enterprise_architecture_knowledge_graph_v5_3_arrows_legend.html).

## Repository contents

| Path | Role |
|------|------|
| `c5_enterprise_architecture_knowledge_graph_v5_3_arrows_legend.html` | Viewer |
| `c5_enterprise_architecture_knowledge_graph_v5_causal_temporal.json` | Graph source |
| `vendor/d3.v7.min.js` | Local D3 v7 (offline) |
| `serve_graph.py` | Local HTTP server |
| `test_graph_viewer_production.py` | Viewer packaging tests |

Edit the JSON and refresh the page. Export buttons write `c5-enterprise-architecture-knowledge-graph-v5.3.{json,graphml,svg}`.

## Development

```bash
python3 -m pip install -r requirements-dev.txt
pre-commit install
pre-commit run --all-files
python3 -m unittest test_graph_viewer_production.py -v
```

CI runs the same pre-commit hooks and tests on `main` and pull requests.

## Licence

MIT. See [LICENSE](LICENSE).
