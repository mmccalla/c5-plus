#!/usr/bin/env python3
"""Validate the graph JSON, the viewer version and the question traversals doc.

Checks that every edge follows the relation catalogue, that inverses are derived
rather than stored, that node descriptions are real definitions, that versions
agree, and that every documented question pattern walks real edges.
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAPH = ROOT / "c5_enterprise_architecture_knowledge_graph_v5_causal_temporal.json"
VIEWER = ROOT / "index.html"
TRAVERSALS = ROOT / "docs" / "question-traversals.md"
IMPACT_VALUES = {"forward", "reverse", None}


def check_ontology(data, errors):
    ontology, catalogue = data["relationshipOntology"], data["relationCatalogue"]
    for label, rel in catalogue.items():
        family = ontology.get(rel["family"])
        if family is None:
            errors.append(f"relation {label!r}: unknown family {rel['family']!r}")
            continue
        if rel["class"] not in family["classes"]:
            errors.append(
                f"relation {label!r}: class {rel['class']!r} is not a class of {rel['family']}"
            )
        if label not in family["relations"]:
            errors.append(f"relation {label!r}: missing from {rel['family']}.relations")
        if rel.get("impact") not in IMPACT_VALUES:
            errors.append(
                f"relation {label!r}: impact must be forward, reverse or null"
            )
        if not rel.get("definition"):
            errors.append(f"relation {label!r}: missing definition")
        inverse = rel.get("inverse")
        if inverse in catalogue:
            other = catalogue[inverse]
            if (other["family"], other["class"]) != (rel["family"], rel["class"]):
                errors.append(
                    f"relation {label!r}: stored inverse {inverse!r} is in a different family or class"
                )
    for name, family in ontology.items():
        expected = sorted(
            label for label, rel in catalogue.items() if rel["family"] == name
        )
        if sorted(family["relations"]) != expected:
            errors.append(f"family {name}: relations list does not match the catalogue")
        transitive = sorted(
            label for label in expected if catalogue[label]["transitive"]
        )
        if sorted(family["transitiveRelations"]) != transitive:
            errors.append(
                f"family {name}: transitiveRelations does not match the catalogue"
            )
    expected_inverses = {
        label: rel["inverse"] for label, rel in catalogue.items() if "inverse" in rel
    }
    if data.get("inverseMap") != expected_inverses:
        errors.append(
            "inverseMap does not match the inverses declared in relationCatalogue"
        )


def check_links(data, errors):
    catalogue = data["relationCatalogue"]
    ids = [n["id"] for n in data["nodes"]]
    node_ids = set(ids)
    for node_id, count in Counter(ids).items():
        if count > 1:
            errors.append(f"duplicate node id {node_id!r}")
    keys = Counter()
    for link in data["links"]:
        s, label, t = link["source"], link["label"], link["target"]
        where = f"edge {s} --{label}-> {t}"
        keys[(s, label, t)] += 1
        if s not in node_ids or t not in node_ids:
            errors.append(f"{where}: unknown node")
        if s == t:
            errors.append(f"{where}: self loop")
        if "inverseOf" in link:
            errors.append(
                f"{where}: stored inverse edge; inverses are derived from relationCatalogue"
            )
        rel = catalogue.get(label)
        if rel is None:
            errors.append(f"{where}: label is not in relationCatalogue")
            continue
        expected = {
            "relationshipFamily": rel["family"],
            "relationshipClass": rel["class"],
            "relationshipSemantics": rel["definition"],
            "transitiveCandidate": rel["transitive"],
            "inverseCandidate": "inverse" in rel,
        }
        for field, value in expected.items():
            if link.get(field) != value:
                errors.append(
                    f"{where}: {field} is {link.get(field)!r}, catalogue says {value!r}"
                )
    for key, count in keys.items():
        if count > 1:
            errors.append(f"duplicate edge {key}")
    for s, label, t in keys:
        inverse = catalogue.get(label, {}).get("inverse")
        if inverse and (t, inverse, s) in keys:
            errors.append(
                f"edge {s} --{label}-> {t} is also stored as its inverse {t} --{inverse}-> {s}"
            )
    used = {link["label"] for link in data["links"]}
    for label in sorted(set(catalogue) - used):
        errors.append(f"relation {label!r} is catalogued but unused")


def check_structural_acyclic(data, errors):
    """Part-whole and subtype edges must not loop. Temporal loops are allowed: they model recurring lifecycles."""
    adjacency = {}
    for link in data["links"]:
        if link["relationshipFamily"] == "Structural":
            adjacency.setdefault(link["source"], []).append(link["target"])
    state = {}

    def visit(node, trail):
        state[node] = "open"
        trail.append(node)
        for nxt in adjacency.get(node, []):
            if state.get(nxt) == "open":
                loop = trail[trail.index(nxt) :] + [nxt]
                errors.append(f"Structural loop: {' -> '.join(loop)}")
            elif nxt not in state:
                visit(nxt, trail)
        trail.pop()
        state[node] = "done"

    for node in list(adjacency):
        if node not in state:
            visit(node, [])


def check_nodes(data, errors):
    descriptions = Counter()
    for node in data["nodes"]:
        text = node.get("description", "").strip()
        descriptions[text] += 1
        if len(text) < 30 or re.fullmatch(r".+ in the .+ domain\.", text):
            errors.append(
                f"node {node['id']!r}: description is a placeholder, not a definition"
            )
    for text, count in descriptions.items():
        if count > 1:
            errors.append(f"{count} nodes share the description {text!r}")
    used = {link["source"] for link in data["links"]} | {
        link["target"] for link in data["links"]
    }
    for node in data["nodes"]:
        if node["id"] not in used:
            errors.append(f"node {node['id']!r} has no edges")


def check_versions(data, errors):
    version = data["projection"]["version"]
    html = VIEWER.read_text(encoding="utf-8")
    found = set(re.findall(r'application-version" content="([^"]+)"', html))
    found |= set(re.findall(r'version:"([^"]+)"', html))
    if found != {version}:
        errors.append(
            f"index.html versions {sorted(found)} do not match graph version {version}"
        )


def check_traversals(data, errors):
    """Every hop in a documented pattern must be a stored edge or a declared inverse of one."""
    catalogue = data["relationCatalogue"]
    stored = {(link["source"], link["label"], link["target"]) for link in data["links"]}
    inverse_of = {}
    for label, rel in catalogue.items():
        if "inverse" in rel:
            inverse_of.setdefault(rel["inverse"], set()).add(label)
    text = TRAVERSALS.read_text(encoding="utf-8")
    patterns = re.findall(r"^\*\*Pattern:\*\* (.+)$", text, flags=re.MULTILINE)
    if not patterns:
        errors.append("docs/question-traversals.md: no patterns found")
    for line in patterns:
        for chain in re.findall(r"`([^`]+)`", line):
            parts = re.split(r" --(.+?)→ ", chain)
            for i in range(0, len(parts) - 2, 2):
                s, label, t = parts[i], parts[i + 1], parts[i + 2]
                if (s, label, t) in stored:
                    continue
                if any(
                    (t, primary, s) in stored for primary in inverse_of.get(label, ())
                ):
                    continue
                errors.append(
                    f"docs/question-traversals.md: hop {s} --{label}→ {t} is neither stored nor a declared inverse"
                )


def main():
    data = json.loads(GRAPH.read_text(encoding="utf-8"))
    errors = []
    check_ontology(data, errors)
    check_links(data, errors)
    check_structural_acyclic(data, errors)
    check_nodes(data, errors)
    check_versions(data, errors)
    check_traversals(data, errors)
    for error in errors:
        print(error)
    if errors:
        print(f"{len(errors)} problem(s) found")
        return 1
    print(
        f"graph OK: {len(data['nodes'])} nodes, {len(data['links'])} edges, {len(data['relationCatalogue'])} relations"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
