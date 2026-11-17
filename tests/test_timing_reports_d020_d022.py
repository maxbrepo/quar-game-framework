import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class TimingReportsTests(unittest.TestCase):
    def test_demo_contracts(self):
        for n in range(20, 23):
            with self.subTest(demo=n):
                matches = list((ROOT / "demos/0.0.2/01_core").glob(f"{n:03d}_*/main.vq"))
                self.assertEqual(len(matches), 1)
                source = matches[0].read_text()
                meta = json.loads(matches[0].with_name("demo.json").read_text())
                self.assertEqual(meta["id"], f"{n:03d}")
                self.assertIn("bool batch_mode = false;", source)
                self.assertIn('print("QGF_DEMO_OK");', source)
                self.assertIn("SDL_DestroyRenderer(renderer);", source)
                self.assertIn("SDL_DestroyWindow(window);", source)

    def test_semantic_analysis(self):
        import sys
        sdk = ROOT / "sdk"
        if not (sdk / "frontend/quar/lexer.py").exists():
            self.skipTest("SDK not available")
        sys.path.insert(0, str(sdk))
        from frontend.quar.lexer import Lexer
        from frontend.quar.parser import Parser
        from frontend.quar.semantic import SemanticAnalyzer
        for n in range(20, 23):
            path = next((ROOT / "demos/0.0.2/01_core").glob(f"{n:03d}_*/main.vq"))
            with self.subTest(demo=n):
                SemanticAnalyzer().analyze(Parser(Lexer(path.read_text()).tokenize()).parse())

if __name__ == "__main__":
    unittest.main()
