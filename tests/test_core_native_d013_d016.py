"""Static regression checks for QGF Core D013-D016."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class NativeCoreTests(unittest.TestCase):
    def test_sources_and_metadata(self):
        for number in range(13, 17):
            matches = list((ROOT / "demos/0.0.2/01_core").glob(f"{number:03d}_*/demo.json"))
            self.assertEqual(len(matches), 1)
            data = json.loads(matches[0].read_text())
            self.assertEqual(data["id"], f"{number:03d}")
            self.assertEqual(data["chapter"], 1)
            code = matches[0].with_name("main.vq").read_text()
            self.assertIn("SDL_DestroyRenderer(renderer);", code)
            self.assertIn("SDL_DestroyWindow(window);", code)
            self.assertIn('print("QGF_DEMO_OK");', code)

if __name__ == "__main__":
    unittest.main()
