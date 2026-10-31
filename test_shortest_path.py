"""Shortest path is directed and skips the manages trap when another route exists.

Undirected BFS from application component to data object takes the 1-hop
manages edge. The viewer must prefer a directed route that does not use
manages when one exists, and must not isolate a path that does not exist.
"""

from __future__ import annotations

import json
import unittest
from collections import deque
from pathlib import Path

from viewer_runtime import viewer_op

ROOT = Path(__file__).resolve().parent
JSON = ROOT / "c5_enterprise_architecture_knowledge_graph_v5_causal_temporal.json"


def source_id(edge: dict) -> str:
    src = edge["source"]
    return src if isinstance(src, str) else src["id"]


def target_id(edge: dict) -> str:
    tgt = edge["target"]
    return tgt if isinstance(tgt, str) else tgt["id"]


def undirected_shortest(links: list[dict], src: str, tgt: str) -> list[str] | None:
    adj: dict[str, list[str]] = {}
    for edge in links:
        s, t = source_id(edge), target_id(edge)
        adj.setdefault(s, []).append(t)
        adj.setdefault(t, []).append(s)
    prev: dict[str, str | None] = {src: None}
    queue = deque([src])
    while queue:
        current = queue.popleft()
        if current == tgt:
            break
        for node in adj.get(current, []):
            if node not in prev:
                prev[node] = current
                queue.append(node)
    if tgt not in prev:
        return None
    path: list[str] = []
    cursor: str | None = tgt
    while cursor is not None:
        path.append(cursor)
        cursor = prev[cursor]
    path.reverse()
    return path


class ShortestPathTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.links = json.loads(JSON.read_text(encoding="utf-8"))["links"]

    def test_undirected_shortest_takes_the_manages_trap(self) -> None:
        path = undirected_shortest(self.links, "application component", "data object")
        self.assertEqual(path, ["application component", "data object"])

    def test_viewer_shortest_skips_manages_and_isolates_that_path(self) -> None:
        result = viewer_op(
            {
                "op": "shortest",
                "src": "application component",
                "tgt": "data object",
            }
        )
        self.assertTrue(result["found"])
        nodes = result["nodes"]
        self.assertIsNotNone(nodes)
        assert nodes is not None
        self.assertGreaterEqual(len(nodes), 3)
        self.assertEqual(nodes[0], "application component")
        self.assertEqual(nodes[-1], "data object")
        self.assertNotEqual(nodes, ["application component", "data object"])
        self.assertNotIn("manages", result["labels"])
        isolate = result["isolate"]
        self.assertTrue(isolate["restrictToHighlight"])
        self.assertEqual(isolate["nodeIds"], sorted(nodes))
        self.assertTrue(all("manages" not in edge for edge in isolate["edges"]))
        self.assertEqual(len(isolate["edges"]), len(nodes) - 1)

    def test_viewer_shortest_with_no_directed_path_does_not_isolate(self) -> None:
        result = viewer_op({"op": "shortest", "src": "cost", "tgt": "apm"})
        self.assertFalse(result["found"])
        self.assertIsNone(result["nodes"])
        isolate = result["isolate"]
        self.assertFalse(isolate["restrictToHighlight"])
        self.assertIn("No path found under current filters.", isolate["pathHtml"])
        self.assertNotIn("apm", isolate["nodeIds"])
        self.assertIn("cost", isolate["nodeIds"])


if __name__ == "__main__":
    unittest.main()
