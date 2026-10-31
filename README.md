# Which data does this application depend on?

Enterprise and data architects still answer impact, ownership and data-scope questions with slide stacks.
This repo projects those questions as directed traversals over a shared concept model.
It is for EA and data-architecture decisions: impact, productisation, and joining applications to data without a modelling-ticket backlog.

**Live graph:** https://mmccalla.github.io/c5-plus/

**Finding:** From an application component you can reach the data product it consumes and the data object underneath — one directed path instead of three slide layers.

Core questions this model is built to answer (directed walks on the graph, path tools, and verified competency coverage):

1. What depends on this?
2. What will this change impact?
3. Who owns this?
4. Which policies apply?
5. Which customer outcomes are affected?
6. What data is involved?
7. Which teams must be involved?

Not all of these are available from the **English Ask box** — only the seven intents below. The rest are answered via path buttons, Learn Q6, or the wider verified competency set (see tests and local `question_set.md` if present).

This is a concept projection (metamodel), not a populated client estate, and no graph database is required to inspect the static viewer.

How the graph walks (directed patterns, including inverses): [docs/question-traversals.md](docs/question-traversals.md)

## English Ask (local reasoner)

GitHub Pages serves the static viewer only. To use **Ask in English**, run the reasoner locally; it serves the viewer and `POST /ask` on port **8765**.

```bash
python3 -m pip install -r requirements-ask.txt
python3 -m ask
```

Open [http://127.0.0.1:8765/](http://127.0.0.1:8765/). Health: `GET /health` → `{"status":"ok"}`.

Ask is **not** open chat. Your sentence must match a regex in [ask/compile_nl.py](ask/compile_nl.py) (`INTENT_PATTERNS`). The `…` slot must resolve to **exactly one** node id from the projection JSON (longest gazetteer match wins). Misses return HTTP **422** with `error` and `candidates`.

| Intent | Example shapes (paraphrase only within the regex) |
|--------|---------------------------------------------------|
| `depends_on` | What does … depend on? |
| `dependents` | What depends on …? · Who depends on …? · Dependents of … |
| `owns` | Who owns …? |
| `policies` | Which policies apply to …? · What policies apply to …? |
| `realisation` | How is … realised? · How is … realized? |
| `sequence` | What happens after …? · What happens next …? |
| `impact` | What will be/is/gets impacted if I/we change …? · What will changing … impact? · Impact of changing … |

Worked compile examples: [test_ask_compile.py](test_ask_compile.py) (`GOLDEN_IR`). SPARQL for each intent: [ask/intents.py](ask/intents.py).

**Seed naming:** use graph node ids (e.g. `application component`, `data product`). Synonyms that are not node ids (e.g. “software component”) may match a shorter id such as `component` and yield a different blast than you expect.

## Repository

These are the files GitHub serves and deploys. Local scratch files are not listed here.

| Path | Role |
|------|------|
| [index.html](index.html) | Viewer |
| [c5_enterprise_architecture_knowledge_graph_v5_causal_temporal.json](c5_enterprise_architecture_knowledge_graph_v5_causal_temporal.json) | Graph source |
| [vendor/d3.v7.min.js](vendor/d3.v7.min.js) | Vendored D3 v7 |
| [favicon.svg](favicon.svg), [favicon.ico](favicon.ico), [apple-touch-icon.png](apple-touch-icon.png) | Site icons |
| [docs/question-traversals.md](docs/question-traversals.md) | directed question patterns |
| [ask/](ask/) | English → Query IR compile, OWL-RL SPARQL reasoner, local viewer server |
| [requirements-ask.txt](requirements-ask.txt) | Reasoner runtime (rdflib, owlrl, FastAPI) |
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
