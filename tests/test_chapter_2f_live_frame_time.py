"""Static checks for the live frame-time demo. Does not replace QRVM tests."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "demos/0.0.2/02_game_loop/006_live_frame_time"

class LiveFrameTimeContract(unittest.TestCase):
    def test_metadata(self):
        data = json.loads((DEMO / "demo.json").read_text())
        self.assertEqual(data["chapter"], 2)
        self.assertEqual(data["id"], "006")

    def test_interval_counter_includes_current_frame(self):
        source = (DEMO / "main.vq").read_text()
        increment = source.index("monitor_frames = monitor_frames + one_frame;")
        measurement = source.index("u64 monitor_elapsed_ms")
        self.assertLess(increment, measurement)
        self.assertIn("monitor_elapsed_ms / monitor_frames", source)
        self.assertIn('print("QGF_DEMO_OK")', source)

if __name__ == "__main__":
    unittest.main()
