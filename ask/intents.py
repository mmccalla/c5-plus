"""SPARQL templates for closed-graph Query IR intents."""

from __future__ import annotations

import json
from collections import deque
from collections.abc import Iterable
from typing import Any

from rdflib import Graph, URIRef

from ask.json_to_rdf import CONCEPT, DEFAULT_JSON, REL, concept_iri, load_graph, slug

CONCEPT_PREFIX = str(CONCEPT)
REL_PREFIX = str(REL)

DEPENDENCY_PRIMARY = frozenset({"uses", "requires", "consumes", "calls"})
DEPENDENCY_INVERSE = frozenset({"used by", "depended on by"})
REALISATION_LABELS = frozenset({"realised by", "exposed via"})
# Inverse-worded causal: the seed is the influencer, so changing it hits the source.
IMPACT_INFLUENCE_INBOUND = frozenset({"driven by", "aligns to", "guided by"})
SEQUENCE_WALK_LABELS = frozenset(
    {
        "precedes",
        "triggers",
        "followed by",
        "produces next",
    }
)
SEQUENCE_MODAL_LABELS = frozenset({"can precede", "may trigger"})
STRUCT_LABELS = frozenset(
    {"contains", "comprises", "includes", "has", "part of", "partitioned into"}
)


def _catalogue() -> tuple[dict[str, str], dict[str, str], frozenset[str]]:
    data = json.loads(DEFAULT_JSON.read_text(encoding="utf-8"))
    nodes: dict[str, str] = {}
    labels: dict[str, str] = {}
    causal: set[str] = set()
    for node in data["nodes"]:
        node_id = node["id"]
        nodes[slug(node_id)] = node_id
    for edge in data["links"]:
        labels[slug(edge["label"])] = edge["label"]
        if edge["relationshipFamily"] == "Causal":
            causal.add(edge["label"])
        for key in ("source", "target"):
            raw = edge[key]
            node_id = raw if isinstance(raw, str) else raw["id"]
            nodes[slug(node_id)] = node_id
    for forward, reverse in data["inverseMap"].items():
        labels[slug(forward)] = forward
        labels[slug(reverse)] = reverse
    return nodes, labels, frozenset(causal)


_NODES, _LABELS, _CAUSAL = _catalogue()
IMPACT_OUTBOUND = _CAUSAL | REALISATION_LABELS | STRUCT_LABELS | DEPENDENCY_INVERSE
IMPACT_INBOUND = (
    REALISATION_LABELS | STRUCT_LABELS | DEPENDENCY_PRIMARY | IMPACT_INFLUENCE_INBOUND
)


def _sparql_in(labels: Iterable[str]) -> str:
    return ", ".join(f"rel:{slug(label)}" for label in sorted(labels))


# Dependents must query these CURIEs. A Python inbound-uses rewrite is not enough.
DEPENDENTS_SPARQL = f"""
PREFIX rel: <{REL_PREFIX}>
SELECT DISTINCT ?source ?predicate ?target WHERE {{
  {{
    ?seed ?predicate ?target .
    FILTER(?predicate IN (rel:used-by, rel:depended-on-by))
    BIND(?seed AS ?source)
  }}
  UNION
  {{
    ?source ?predicate ?seed .
    FILTER(?predicate IN (rel:uses, rel:requires, rel:consumes, rel:calls))
    BIND(?seed AS ?target)
  }}
  FILTER(STRSTARTS(STR(?source), "{CONCEPT_PREFIX}"))
  FILTER(STRSTARTS(STR(?target), "{CONCEPT_PREFIX}"))
}}
"""

DEPENDS_ON_SPARQL = f"""
PREFIX rel: <{REL_PREFIX}>
SELECT DISTINCT ?source ?predicate ?target WHERE {{
  BIND(?seed AS ?source)
  ?source ?predicate ?target .
  FILTER(?predicate IN (rel:uses, rel:requires, rel:consumes, rel:calls))
  FILTER(STRSTARTS(STR(?target), "{CONCEPT_PREFIX}"))
}}
"""

OWNS_SPARQL = f"""
PREFIX rel: <{REL_PREFIX}>
SELECT DISTINCT ?source ?predicate ?target WHERE {{
  {{
    ?seed ?predicate ?target .
    FILTER(?predicate IN (rel:owned-by, rel:accountable-steward))
    BIND(?seed AS ?source)
  }}
  UNION
  {{
    ?source ?predicate ?seed .
    FILTER(?predicate IN (rel:owns, rel:accountable-for))
    BIND(?seed AS ?target)
  }}
  FILTER(STRSTARTS(STR(?source), "{CONCEPT_PREFIX}"))
  FILTER(STRSTARTS(STR(?target), "{CONCEPT_PREFIX}"))
}}
"""

POLICIES_SPARQL = f"""
PREFIX rel: <{REL_PREFIX}>
SELECT DISTINCT ?source ?predicate ?target WHERE {{
  {{
    ?source ?predicate ?seed .
    FILTER(?predicate IN (rel:governs, rel:applied-to))
    BIND(?seed AS ?target)
  }}
  UNION
  {{
    ?seed ?predicate ?target .
    FILTER(?predicate IN (rel:governed-by, rel:restricted-by, rel:constrained-by))
    BIND(?seed AS ?source)
  }}
  UNION
  {{
    {{
      ?source ?link ?seed .
      FILTER(?link IN (rel:governs, rel:applied-to))
    }}
    UNION
    {{
      ?seed ?link ?source .
      FILTER(?link IN (rel:governed-by, rel:restricted-by, rel:constrained-by))
    }}
    ?source rel:enforced-by ?target .
    BIND(rel:enforced-by AS ?predicate)
  }}
  FILTER(STRSTARTS(STR(?source), "{CONCEPT_PREFIX}"))
  FILTER(STRSTARTS(STR(?target), "{CONCEPT_PREFIX}"))
}}
"""

REALISATION_SPARQL = f"""
PREFIX rel: <{REL_PREFIX}>
SELECT DISTINCT ?source ?predicate ?target ?neighbor WHERE {{
  ?seed ?predicate ?neighbor .
  FILTER(?predicate IN ({_sparql_in(REALISATION_LABELS)}))
  BIND(?seed AS ?source)
  BIND(?neighbor AS ?target)
  FILTER(STRSTARTS(STR(?neighbor), "{CONCEPT_PREFIX}"))
}}
"""

SEQUENCE_SPARQL = f"""
PREFIX rel: <{REL_PREFIX}>
SELECT DISTINCT ?source ?predicate ?target ?neighbor WHERE {{
  ?seed ?predicate ?neighbor .
  FILTER(?predicate IN ({_sparql_in(SEQUENCE_WALK_LABELS)}))
  BIND(?seed AS ?source)
  BIND(?neighbor AS ?target)
  FILTER(STRSTARTS(STR(?neighbor), "{CONCEPT_PREFIX}"))
}}
"""

SEQUENCE_MODAL_SPARQL = f"""
PREFIX rel: <{REL_PREFIX}>
SELECT DISTINCT ?source ?predicate ?target WHERE {{
  BIND(?seed AS ?source)
  ?source ?predicate ?target .
  FILTER(?predicate IN ({_sparql_in(SEQUENCE_MODAL_LABELS)}))
  FILTER(STRSTARTS(STR(?target), "{CONCEPT_PREFIX}"))
}}
"""

IMPACT_SPARQL = f"""
PREFIX rel: <{REL_PREFIX}>
SELECT DISTINCT ?source ?predicate ?target ?neighbor WHERE {{
  {{
    ?seed ?predicate ?neighbor .
    FILTER(?predicate IN ({_sparql_in(IMPACT_OUTBOUND)}))
    BIND(?seed AS ?source)
    BIND(?neighbor AS ?target)
  }}
  UNION
  {{
    ?neighbor ?predicate ?seed .
    FILTER(?predicate IN ({_sparql_in(IMPACT_INBOUND)}))
    BIND(?neighbor AS ?source)
    BIND(?seed AS ?target)
  }}
  FILTER(STRSTARTS(STR(?source), "{CONCEPT_PREFIX}"))
  FILTER(STRSTARTS(STR(?target), "{CONCEPT_PREFIX}"))
  FILTER(STRSTARTS(STR(?neighbor), "{CONCEPT_PREFIX}"))
}}
"""


def _node_id(term: URIRef) -> str:
    key = str(term)[len(CONCEPT_PREFIX) :]
    try:
        return _NODES[key]
    except KeyError as exc:
        raise ValueError(f"unknown concept IRI: {term}") from exc


def _label(term: URIRef) -> str:
    key = str(term)[len(REL_PREFIX) :]
    try:
        return _LABELS[key]
    except KeyError as exc:
        raise ValueError(f"unknown rel IRI: {term}") from exc


def _run(graph: Graph, query: str, seed: str) -> list[tuple[URIRef, URIRef, URIRef]]:
    rows: list[tuple[URIRef, URIRef, URIRef]] = []
    for row in graph.query(query, initBindings={"seed": concept_iri(seed)}):
        rows.append((row.source, row.predicate, row.target))
    return rows


def _walk(graph: Graph, seed: str, query: str) -> list[tuple[URIRef, URIRef, URIRef]]:
    """Directed multi-hop with a cycle-safe visited set; each step is SPARQL."""
    start = concept_iri(seed)
    visited = {start}
    frontier: deque[URIRef] = deque([start])
    rows: list[tuple[URIRef, URIRef, URIRef]] = []
    seen: set[tuple[URIRef, URIRef, URIRef]] = set()
    while frontier:
        current = frontier.popleft()
        for row in graph.query(query, initBindings={"seed": current}):
            key = (row.source, row.predicate, row.target)
            if key in seen:
                continue
            seen.add(key)
            rows.append(key)
            neighbor = row.neighbor
            if neighbor not in visited:
                visited.add(neighbor)
                frontier.append(neighbor)
    return rows


def _shape(
    rows: Iterable[tuple[URIRef, URIRef, URIRef]], asserted: Graph
) -> list[dict[str, Any]]:
    hops: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for source, predicate, target in rows:
        hop = {
            "source": _node_id(source),
            "label": _label(predicate),
            "target": _node_id(target),
            "inferred": (source, predicate, target) not in asserted,
        }
        key = (hop["source"], hop["label"], hop["target"])
        if key in seen:
            continue
        seen.add(key)
        hops.append(hop)
    hops.sort(key=lambda hop: (hop["source"], hop["label"], hop["target"]))
    return hops


def execute(ir: dict[str, str], closed_graph: Graph) -> list[dict[str, Any]]:
    """Run a closed Query IR against an already-closed graph and flag inferred hops."""
    intent = ir["intent"]
    seed = ir["seed"]
    asserted = load_graph()
    runners = {
        "dependents": lambda: _run(closed_graph, DEPENDENTS_SPARQL, seed),
        "depends_on": lambda: _run(closed_graph, DEPENDS_ON_SPARQL, seed),
        "owns": lambda: _run(closed_graph, OWNS_SPARQL, seed),
        "policies": lambda: _run(closed_graph, POLICIES_SPARQL, seed),
        "realisation": lambda: _walk(closed_graph, seed, REALISATION_SPARQL),
        "sequence": lambda: (
            _walk(asserted, seed, SEQUENCE_SPARQL)
            + _run(asserted, SEQUENCE_MODAL_SPARQL, seed)
        ),
        "impact": lambda: _walk(closed_graph, seed, IMPACT_SPARQL),
    }
    try:
        runner = runners[intent]
    except KeyError as exc:
        raise ValueError(f"unknown intent: {intent}") from exc
    return _shape(runner(), asserted)
