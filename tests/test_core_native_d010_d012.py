"""Checks for QGF native Core demo candidates D010-D012."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SDK = ROOT / "sdk"

class CoreNativeDemoTests(unittest.TestCase):
    def test_demo_metadata(self):
        for number in range(10, 13):
            demos = list((ROOT / "demos" / "0.0.2" / "01_core").glob(f"{number:03d}_*/demo.json"))
            self.assertEqual(len(demos), 1)
            metadata = json.loads(demos[0].read_text())
            self.assertEqual(metadata["chapter"], 1)
            self.assertEqual(metadata["version"], "0.0.2")
            source = demos[0].with_name("main.vq").read_text()
            self.assertIn('bool batch_mode = false;', source)
            self.assertIn('print("QGF_DEMO_OK");', source)

    def test_semantic_analysis(self):
        if not (SDK / "frontend" / "quar" / "lexer.py").exists():
            self.skipTest("External SDK not available")
        sys.path.insert(0, str(SDK))
        from frontend.quar.lexer import Lexer
        from frontend.quar.parser import Parser
        from frontend.quar.semantic import SemanticAnalyzer
        for number in range(10, 13):
            source_path = next((ROOT / "demos" / "0.0.2" / "01_core").glob(f"{number:03d}_*/main.vq"))
            with self.subTest(demo=number):
                tree = Parser(Lexer(source_path.read_text()).tokenize()).parse()
                SemanticAnalyzer().analyze(tree)

if __name__ == "__main__":
    unittest.main()
