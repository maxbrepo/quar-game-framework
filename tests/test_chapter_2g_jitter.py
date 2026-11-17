"""Static contract checks; native QRVM execution is not covered."""
import json
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "demos/0.0.2/02_game_loop/007_frame_jitter_monitor"
class JitterContract(unittest.TestCase):
    def test_metadata(self):
        d = json.loads((DEMO / "demo.json").read_text())
        self.assertEqual((d["chapter"], d["id"]), (2, "007"))
    def test_min_max_reset(self):
        s = (DEMO / "main.vq").read_text()
        for token in ("interval_min_ms", "interval_max_ms", "has_interval_sample = false;", 'print("QGF_DEMO_OK")'):
            self.assertIn(token, s)
        self.assertLess(s.index("if (delta_ms < interval_min_ms)"), s.index('print("Minimum observed'))
if __name__ == "__main__": unittest.main()
