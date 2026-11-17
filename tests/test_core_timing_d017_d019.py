"""Validate QGF native timing demonstration sources."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SDK = ROOT / "sdk"

class TimingDemosTests(unittest.TestCase):
    def test_metadata_and_markers(self):
        for number in range(17, 20):
            with self.subTest(number=number):
                matches = list((ROOT / "demos/0.0.2/01_core").glob(f"{number:03d}_*/main.vq"))
                self.assertEqual(len(matches), 1)
                source = matches[0].read_text()
                meta = json.loads(matches[0].with_name("demo.json").read_text())
                self.assertEqual(meta["id"], f"{number:03d}")
                self.assertIn("bool batch_mode = false;", source)
                self.assertIn('print("QGF_DEMO_OK");', source)
                self.assertIn("SDL_DestroyWindow(window);", source)

    def test_semantic_analysis(self):
        if not (SDK / "frontend/quar/lexer.py").exists():
            self.skipTest("External Visual Quar SDK not available")
        sys.path.insert(0, str(SDK))
        from frontend.quar.lexer import Lexer
        from frontend.quar.parser import Parser
        from frontend.quar.semantic import SemanticAnalyzer
        for number in range(17, 20):
            path = next((ROOT / "demos/0.0.2/01_core").glob(f"{number:03d}_*/main.vq"))
            with self.subTest(number=number):
                SemanticAnalyzer().analyze(Parser(Lexer(path.read_text()).tokenize()).parse())

if __name__ == "__main__":
    unittest.main()
