"""Regression coverage for multiple lifecycle frame limits."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "demos/0.0.2/01_core/008_sequential_windows/main.vq"
META = SOURCE.with_name("demo.json")


class SequentialLifecycleTests(unittest.TestCase):
    def test_both_loops_have_canonical_limits(self):
        self.assertEqual(SOURCE.read_text().count("if (frame_count >= 60)"), 2)

    def test_cleanup_order(self):
        text = SOURCE.read_text()
        self.assertEqual(text.count("SDL_DestroyRenderer(renderer);"), 2)
        self.assertEqual(text.count("SDL_DestroyWindow(window);"), 2)
        self.assertLess(text.rfind("SDL_DestroyWindow(window);"), text.rfind("SDL_Quit();"))

    def test_metadata(self):
        data = json.loads(META.read_text())
        self.assertEqual((data["version"], data["chapter"], data["id"]), ("0.0.2", 1, "008"))

    def test_runner_supports_multiple_limits(self):
        source = (ROOT / "main.py").read_text()
        self.assertIn('content.replace(frame_marker, f"if (frame_count >= {frames})")', source)


if __name__ == "__main__":
    unittest.main()
