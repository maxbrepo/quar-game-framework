"""Regression checks for the versioned D003 graphical demo."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import main

class D003Tests(unittest.TestCase):
    def test_versioned_discovery(self):
        demos = main.discover_demos()
        self.assertIn("0.0.2/01_core/003_bouncing_cross", demos)
        self.assertEqual(main.resolve_demo("003_bouncing_cross", demos), "0.0.2/01_core/003_bouncing_cross")

    def test_metadata(self):
        source = main.discover_demos()["0.0.2/01_core/003_bouncing_cross"]
        data = json.loads((source.parent / "demo.json").read_text())
        self.assertEqual(data["chapter"], 1)
        self.assertEqual(data["version"], "0.0.2")
        self.assertEqual(data["batch_frames"], 60)

    def test_smoke_marker(self):
        source = main.discover_demos()["0.0.2/01_core/003_bouncing_cross"]
        content = source.read_text()
        self.assertEqual(content.count("bool batch_mode = false;"), 1)
        self.assertIn("QGF_DEMO_OK", content)
        self.assertIn("SDL_RenderLine", content)

if __name__ == "__main__":
    unittest.main()
