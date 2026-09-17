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
