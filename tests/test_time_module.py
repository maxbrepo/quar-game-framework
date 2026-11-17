"""Check the QGF Time public surface without requiring an SDL3 installation."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TimeModuleTests(unittest.TestCase):
    def test_time_api_is_present(self):
        source = (ROOT / "core" / "time.vq").read_text(encoding="utf-8")
        for name in (
            "qgf_time_interval_valid", "qgf_time_elapsed_ms",
            "qgf_time_delta_ms", "qgf_time_average_fps",
            "qgf_time_average_frame_ms", "qgf_time_frame_budget_overrun_ms",
        ):
            with self.subTest(name=name):
                self.assertIn(name + "(", source)

    def test_no_backend_dependency(self):
        source = (ROOT / "core" / "time.vq").read_text(encoding="utf-8")
        self.assertNotIn('extern "C"', source)
        self.assertNotIn("SDL_Get", source)


if __name__ == "__main__":
    unittest.main()
