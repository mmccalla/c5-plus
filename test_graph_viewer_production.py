"""Contract tests for the v5.3 graph viewer production packaging."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "c5_enterprise_architecture_knowledge_graph_v5_3_arrows_legend.html"
JSON = ROOT / "c5_enterprise_architecture_knowledge_graph_v5_causal_temporal.json"
D3 = ROOT / "vendor" / "d3.v7.min.js"

EXPORT_STEM = "c5-enterprise-architecture-knowledge-graph-v5.3"


class GraphViewerProductionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = HTML.read_text(encoding="utf-8")

    def test_d3_is_vendored_locally_not_loaded_from_cdn(self):
        self.assertNotIn("d3js.org", self.html)
        self.assertNotRegex(self.html, r'src="https?://')
        self.assertIn('src="vendor/d3.v7.min.js"', self.html)
        self.assertTrue(D3.is_file(), "vendor/d3.v7.min.js is missing")
        self.assertGreater(D3.stat().st_size, 50_000)
        self.assertIn("d3", D3.read_text(encoding="utf-8", errors="ignore")[:2000])

    def test_export_filenames_use_current_version(self):
        self.assertNotIn("enterprise-architecture-knowledge-graph-v4", self.html)
        for ext in ("json", "graphml", "svg"):
            self.assertIn(f"{EXPORT_STEM}.{ext}", self.html)

    def test_graph_data_is_fetched_from_canonical_json(self):
        self.assertIsNone(
            re.search(r"const originalData\s*=\s*\{", self.html),
            "Graph data is still baked into the HTML",
        )
        self.assertIn(JSON.name, self.html)
        self.assertRegex(self.html, r"fetch\(")
        self.assertTrue(JSON.is_file())

    def test_build_metadata_is_declared(self):
        self.assertRegex(
            self.html, r'<meta name="application-version" content="5\.3\.0"'
        )
        self.assertRegex(
            self.html,
            r'<meta name="graph-source" content="c5_enterprise_architecture_knowledge_graph_v5_causal_temporal\.json"',
        )
        self.assertRegex(
            self.html, r'<meta name="build-date" content="\d{4}-\d{2}-\d{2}"'
        )
        self.assertIn('id="buildMeta"', self.html)
        self.assertIn("const BUILD", self.html)
        self.assertIn("5.3.0", self.html)


if __name__ == "__main__":
    unittest.main()
