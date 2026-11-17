"""Regression checks for typed SDL3 coordinates and runner completion."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class DemoSemanticRegression(unittest.TestCase):
    def test_render_coordinates_are_not_untyped_float_literals(self):
        for number in ("005", "006", "007"):
            source = next((ROOT / "demos/0.0.2/01_core").glob(number + "*/main.vq")).read_text()
            for line in source.splitlines():
                if "SDL_RenderLine(renderer," in line or "SDL_RenderPoint(renderer," in line:
                    import re
                    self.assertIsNone(re.search(r"(?<![\w.])\d+\.\d+(?!\w)", line), line)

    def test_runner_requires_success_marker_for_interactive_and_batch(self):
        source = (ROOT / "main.py").read_text()
        self.assertIn('capture_output=True, timeout=15 if smoke else None', source)
        self.assertIn("success = demo_execution_succeeded(result)", source)

if __name__ == "__main__":
    unittest.main()
