"""The viewer isolate set is whatever filtered() returns after the real JS walk.

Static identifier checks in index.html cannot prove this: the three Q6 nodes
also share a manages edge, so a walk that names the right hops can still
isolate the trap.
"""

from __future__ import annotations

import unittest

from viewer_runtime import viewer_op

Q6_HOPS = [
    {
        "source": "application component",
        "label": "consumes",
        "target": "data product",
        "inferred": False,
    },
    {
        "source": "data product",
        "label": "uses",
        "target": "data object",
        "inferred": False,
    },
]


class ViewerRuntimeTest(unittest.TestCase):
    def test_show_walk_q6_hops_isolate_consumes_and_uses_not_manages(self) -> None:
        result = viewer_op(
            {
                "op": "showWalk",
                "focus": "application component",
                "title": "Q6",
                "hops": Q6_HOPS,
            }
        )
        isolate = result["isolate"]
        self.assertTrue(isolate["restrictToHighlight"])
        self.assertEqual(
            isolate["nodeIds"],
            ["application component", "data object", "data product"],
        )
        self.assertEqual(
            isolate["edges"],
            [
                "application component|consumes|data product",
                "data product|uses|data object",
            ],
        )
        self.assertNotIn("application component|manages|data object", isolate["edges"])
        self.assertIn("--consumes→", isolate["pathHtml"])
        self.assertIn("--uses→", isolate["pathHtml"])
        self.assertNotIn("manages", isolate["pathHtml"])

    def test_show_walk_draws_inferred_hops_that_are_not_stored_links(self) -> None:
        result = viewer_op(
            {
                "op": "showWalk",
                "focus": "data object",
                "title": "inferred used-by",
                "hops": [
                    {
                        "source": "data object",
                        "label": "used by",
                        "target": "data product",
                        "inferred": True,
                    }
                ],
            }
        )
        isolate = result["isolate"]
        self.assertEqual(isolate["nodeIds"], ["data object", "data product"])
        self.assertEqual(isolate["edges"], ["data object|used by|data product"])
        self.assertIn("inferred", isolate["pathHtml"])

    def test_empty_hops_keep_focus_and_show_honesty(self) -> None:
        result = viewer_op(
            {
                "op": "showWalk",
                "focus": "data product",
                "title": "Who owns this?",
                "hops": [],
            }
        )
        isolate = result["isolate"]
        self.assertEqual(isolate["nodeIds"], ["data product"])
        self.assertEqual(isolate["edges"], [])
        self.assertIn("No stored hops for this question.", isolate["pathHtml"])


if __name__ == "__main__":
    unittest.main()
