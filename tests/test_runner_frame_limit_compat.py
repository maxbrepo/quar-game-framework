"""Regression checks for canonical batch limits in historical and newer demos."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class FrameLimitCompatibilityTests(unittest.TestCase):
    def test_all_demo_frame_limits_are_recognized(self):
        for meta in (ROOT / 'demos').rglob('demo.json'):
            source = (meta.parent / 'main.vq').read_text(encoding='utf-8')
            frames = json.loads(meta.read_text(encoding='utf-8'))['batch_frames']
            self.assertTrue(1 <= frames <= 3600)
            literal = 'if (frame_count >= 60)' in source
            variable = 'if (frame_count >= max_frames)' in source and bool(re.search(r'\bu64 max_frames = [0-9]+;', source))
            self.assertTrue(literal or variable, str(meta))

if __name__ == '__main__':
    unittest.main()
