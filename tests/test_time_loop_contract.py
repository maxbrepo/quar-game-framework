"""Static contract checks for the backend-independent QGF timing layer."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class TimeLoopContractTests(unittest.TestCase):
    def test_loop_helpers_exist(self):
        source = (ROOT / "core" / "time.vq").read_text(encoding="utf-8")
        for name in (
            "qgf_time_clamped_delta_ms", "qgf_time_target_frame_ms",
            "qgf_time_remaining_frame_ms", "qgf_time_instant_fps",
        ):
            with self.subTest(name=name):
                self.assertIn(name + "(", source)

    def test_backend_is_separate(self):
        source = (ROOT / "core" / "time.vq").read_text(encoding="utf-8")
        self.assertNotIn('extern "C"', source)
        self.assertNotIn("SDL_", source)

if __name__ == "__main__":
    unittest.main()
