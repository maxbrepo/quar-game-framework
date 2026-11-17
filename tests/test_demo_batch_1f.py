"""Discovery and structural checks for the chapter 1F demo batch."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import main

class DemoBatch1FTests(unittest.TestCase):
    def test_all_new_demos_discovered(self):
        demos = main.discover_demos()
        for index in range(4, 8):
            self.assertEqual(len([key for key in demos if key.startswith("0.0.2/01_core/") and key.split("/")[-1].startswith(f"{index:03d}_")]), 1)

    def test_batch_metadata_and_cleanup(self):
        for index in range(4, 8):
            source = next(path for key, path in main.discover_demos().items() if key.startswith("0.0.2/01_core/") and key.split("/")[-1].startswith(f"{index:03d}_"))
            metadata = json.loads((source.parent / "demo.json").read_text())
            content = source.read_text()
            self.assertEqual(metadata["chapter"], 1)
            self.assertEqual(metadata["batch_frames"], 60)
            for token in ("SDL_DestroyRenderer(renderer)", "SDL_DestroyWindow(window)", "SDL_Quit()", "QGF_DEMO_OK", "if (frame_count >= 60)"):
                self.assertIn(token, content)

if __name__ == "__main__":
    unittest.main()
