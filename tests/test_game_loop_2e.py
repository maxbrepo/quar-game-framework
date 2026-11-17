"""Static contract checks for chapter 2E demos (no SDK required)."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMO_ROOT = ROOT / "demos/0.0.2/02_game_loop"

class GameLoop2ETests(unittest.TestCase):
    def test_live_fps_uses_elapsed_time(self):
        src = (DEMO_ROOT / "004_live_fps_monitor/main.vq").read_text()
        self.assertIn("monitor_elapsed_ms", src)
        self.assertIn("monitor_frames * ms_per_second", src)
        self.assertIn('print("Live FPS (last interval):")', src)

    def test_motion_is_proportional_to_elapsed_ms(self):
        src = (DEMO_ROOT / "005_delta_scaled_motion/main.vq").read_text()
        self.assertIn("while (movement_ticks < delta_ms)", src)
        self.assertIn("motion_x = motion_x + distance_per_ms", src)
        self.assertIn("u64 max_delta_ms = 50;", src)

    def test_no_untyped_sdl_delay(self):
        for folder in ("004_live_fps_monitor", "005_delta_scaled_motion"):
            src = (DEMO_ROOT / folder / "main.vq").read_text()
            self.assertNotIn("SDL_Delay(1)", src)
            self.assertIn("SDL_Delay(delay_ms)", src)

if __name__ == "__main__":
    unittest.main()
