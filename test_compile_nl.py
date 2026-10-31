"""English questions compile to a closed Query IR, then the graph answers."""

from __future__ import annotations

import unittest

from ask.compile_nl import compile
from ask.intents import execute
from ask.json_to_rdf import load_graph
from ask.reason import close


class CompileImpactPhrasingTests(unittest.TestCase):
    def test_what_will_be_impacted_if_i_change_product_strategy(self) -> None:
        self.assertEqual(
            compile("What will be impacted if I change product strategy?"),
            {"intent": "impact", "seed": "product strategy"},
        )

    def test_what_will_changing_product_strategy_impact_still_compiles(self) -> None:
        self.assertEqual(
            compile("What will changing product strategy impact?"),
            {"intent": "impact", "seed": "product strategy"},
        )


class ImpactProductStrategyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.closed = close(load_graph())

    def test_changing_product_strategy_returns_driven_and_aligned_hops(self) -> None:
        hops = execute({"intent": "impact", "seed": "product strategy"}, self.closed)
        self.assertGreater(len(hops), 0)
        nodes: set[str] = set()
        for hop in hops:
            nodes.add(hop["source"])
            nodes.add(hop["target"])
        self.assertIn("product team", nodes)
        self.assertIn("value proposition statement", nodes)
        labels_on_seed = {
            (hop["source"], hop["label"], hop["target"])
            for hop in hops
            if hop["source"] == "product strategy"
            or hop["target"] == "product strategy"
        }
        self.assertIn(("product team", "driven by", "product strategy"), labels_on_seed)
        self.assertIn(
            ("value proposition statement", "aligns to", "product strategy"),
            labels_on_seed,
        )


if __name__ == "__main__":
    unittest.main()
