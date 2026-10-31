"""SPARQL intents and graph_paths.py must agree on shared 1-hop predicates.

MECE / traversal tests walk graph_paths. Ask walks OWL-RL SPARQL. A silent
split would let the UI answer a different question from the documented walks.
Impact and realisation are allowed to differ; those contracts are explicit.
"""

from __future__ import annotations

import json
import unittest
from collections.abc import Callable
from pathlib import Path

from ask.intents import execute
from ask.json_to_rdf import load_graph
from ask.reason import close
from graph_paths import (
    change_impact_edges,
    depends_on_this_edges,
    mentioned_nodes,
    policies_apply_edges,
    realisation_edges,
    this_depends_on_edges,
    who_owns_edges,
)

ROOT = Path(__file__).resolve().parent
JSON = ROOT / "c5_enterprise_architecture_knowledge_graph_v5_causal_temporal.json"

Walker = Callable[[list[dict], str], list[dict]]

SHARED: list[tuple[str, str, Walker]] = [
    ("dependents", "data product", depends_on_this_edges),
    ("dependents", "data object", depends_on_this_edges),
    ("depends_on", "application component", this_depends_on_edges),
    ("depends_on", "data product", this_depends_on_edges),
    ("owns", "data product", who_owns_edges),
    ("owns", "application component", who_owns_edges),
    ("owns", "okr", who_owns_edges),
    ("policies", "data product", policies_apply_edges),
]


def hop_nodes(hops: list[dict], seed: str) -> set[str]:
    nodes: set[str] = set()
    for hop in hops:
        nodes.add(hop["source"])
        nodes.add(hop["target"])
    nodes.discard(seed)
    return nodes


class AskGraphPathsParityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.links = json.loads(JSON.read_text(encoding="utf-8"))["links"]
        cls.closed = close(load_graph())

    def test_shared_mece_intents_return_the_same_node_sets(self) -> None:
        mismatches: list[str] = []
        for intent, seed, walker in SHARED:
            ask = hop_nodes(
                execute({"intent": intent, "seed": seed}, self.closed), seed
            )
            paths = mentioned_nodes(walker(self.links, seed), seed)
            if ask != paths:
                mismatches.append(
                    f"{intent} {seed}: ask={sorted(ask)} graph_paths={sorted(paths)}"
                )
        self.assertEqual(mismatches, [], "\n".join(mismatches))

    def test_ask_impact_is_not_graph_paths_causal_only(self) -> None:
        """Ask Impact blast follows realisation; MECE Q2 is outbound causal only."""
        ask = hop_nodes(
            execute({"intent": "impact", "seed": "application component"}, self.closed),
            "application component",
        )
        paths = mentioned_nodes(
            change_impact_edges(self.links, "application component"),
            "application component",
        )
        self.assertEqual(paths, set())
        self.assertIn("container", ask)
        self.assertIn("value stream stage", ask)

    def test_ask_realisation_walks_beyond_one_hop_graph_paths(self) -> None:
        ask = hop_nodes(
            execute(
                {"intent": "realisation", "seed": "business capability"}, self.closed
            ),
            "business capability",
        )
        paths = mentioned_nodes(
            realisation_edges(self.links, "business capability"),
            "business capability",
        )
        self.assertNotIn("application component", paths)
        self.assertIn("application component", ask)
        self.assertTrue(paths <= ask)


if __name__ == "__main__":
    unittest.main()
