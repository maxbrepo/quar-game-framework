"""Regression checks for D009 SDL restart demo."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "demos/0.0.2/01_core/009_sdl_restart"

class SDLRestartDemoTests(unittest.TestCase):
    def test_metadata(self):
        data = json.loads((DEMO / "demo.json").read_text(encoding="utf-8"))
        self.assertEqual(data["chapter"], 1)
        self.assertEqual(data["version"], "0.0.2")
        self.assertEqual(data["batch_frames"], 60)

    def test_two_full_lifecycles(self):
        source = (DEMO / "main.vq").read_text(encoding="utf-8")
        self.assertEqual(source.count("SDL_Init(video_flags)"), 2)
        self.assertEqual(source.count("\nSDL_Quit();"), 2)
        self.assertEqual(source.count("SDL_DestroyWindow(window);"), 2)
        self.assertEqual(source.count("SDL_DestroyRenderer(renderer);"), 2)
        self.assertIn('print("QGF_DEMO_OK");', source)

if __name__ == "__main__":
    unittest.main()
