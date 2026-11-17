"""Core demo runner regression tests (no native SDL3 required)."""
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import main


class CoreDemoTests(unittest.TestCase):
    def test_versioned_demo_preferred_over_legacy(self):
        demos = main.discover_demos()
        self.assertIn("0.0.1/01_core/001_hello_pixels", demos)
        self.assertIn("d001_hello_pixels", demos)

    def test_three_versioned_demos(self):
        demos = main.discover_demos()
        for demo in ("001_hello_pixels", "002_moving_line", "003_bouncing_cross"):
            self.assertEqual(len([key for key in demos if key.endswith("/" + demo)]), 1)

    def test_invalid_library_override_fails_not_skips(self):
        with patch.dict(os.environ, {"QGF_SDL3_LIBRARY": "/nonexistent/qgf_sdl3.so"}):
            self.assertIs(main.run_demo("001_hello_pixels", ROOT, smoke=True), False)

    def test_batch_frames_metadata(self):
        import json
        for source in main.discover_demos().values():
            data = json.loads((source.parent / "demo.json").read_text(encoding="utf-8"))
            self.assertGreater(data["batch_frames"], 0)
            self.assertIn("if (frame_count >= 60)", source.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
