"""The ask process serves the viewer at / so a browser on :8765 is not a 404."""

from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from ask.server import app

GRAPH_JSON = "/c5_enterprise_architecture_knowledge_graph_v5_causal_temporal.json"


class AskServerViewerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_root_serves_viewer_html(self) -> None:
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("text/html", res.headers.get("content-type", ""))
        self.assertIn("askQuery", res.text)
        self.assertIn("EA questions", res.text)

    def test_graph_json_is_available(self) -> None:
        res = self.client.get(GRAPH_JSON)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("nodes", data)
        self.assertIn("links", data)
        self.assertIn("relationshipOntology", data)

    def test_vendor_d3_is_available(self) -> None:
        res = self.client.get("/vendor/d3.v7.min.js")
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(res.content), 1000)

    def test_health_still_ok(self) -> None:
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {"status": "ok"})


if __name__ == "__main__":
    unittest.main()
