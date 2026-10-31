"""Load the published concept-projection JSON as an RDFLib graph."""

from __future__ import annotations

import json
from pathlib import Path

from rdflib import OWL, RDF, Graph, Namespace, URIRef

REL = Namespace("https://c5plus.local/rel/")
CONCEPT = Namespace("https://c5plus.local/concept/")
DEFAULT_JSON = (
    Path(__file__).resolve().parent.parent
    / "c5_enterprise_architecture_knowledge_graph_v5_causal_temporal.json"
)
TRANSITIVE_LABELS = frozenset({"contains", "precedes"})


def slug(value: str) -> str:
    return value.strip().lower().replace(" ", "-")


def rel_iri(label: str) -> URIRef:
    return REL[slug(label)]


def concept_iri(node_id: str) -> URIRef:
    return CONCEPT[slug(node_id)]


def load_graph(path: Path | str | None = None) -> Graph:
    source = Path(path) if path is not None else DEFAULT_JSON
    data = json.loads(source.read_text(encoding="utf-8"))
    graph = Graph()
    graph.bind("rel", REL)

    labels = {edge["label"] for edge in data["links"]}
    for label in labels:
        prop = rel_iri(label)
        graph.add((prop, RDF.type, OWL.ObjectProperty))
        if label in TRANSITIVE_LABELS:
            graph.add((prop, RDF.type, OWL.TransitiveProperty))

    for forward, reverse in data["inverseMap"].items():
        fwd, rev = rel_iri(forward), rel_iri(reverse)
        graph.add((fwd, RDF.type, OWL.ObjectProperty))
        graph.add((rev, RDF.type, OWL.ObjectProperty))
        graph.add((fwd, OWL.inverseOf, rev))
        graph.add((rev, OWL.inverseOf, fwd))

    for edge in data["links"]:
        graph.add(
            (
                concept_iri(edge["source"]),
                rel_iri(edge["label"]),
                concept_iri(edge["target"]),
            )
        )
    return graph
