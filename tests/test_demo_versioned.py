import unittest
from pathlib import Path
from unittest.mock import patch
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import main

class VersionedDemosTests(unittest.TestCase):
    def test_discovery(self):
        demos = main.discover_demos()
        self.assertIn("0.0.1/01_core/001_hello_pixels", demos)
        self.assertIn("0.0.2/01_core/002_moving_line", demos)
        self.assertEqual(main.demo_chapter(demos["0.0.1/01_core/001_hello_pixels"]), 1)

    def test_legacy_aliases(self):
        demos = main.discover_demos()
        self.assertEqual(main.resolve_demo("001_hello_pixels", demos), "0.0.1/01_core/001_hello_pixels")
        self.assertEqual(main.resolve_demo("002_moving_line", demos), "0.0.2/01_core/002_moving_line")
        self.assertIsNone(main.resolve_demo("missing", demos))

    def test_batch_all_and_chapter(self):
        with patch.object(main, "run_demo", return_value=True) as run:
            self.assertTrue(main.run_demo_batch(Path("/tmp"), chapter=1))
            self.assertEqual(run.call_count, sum(main.demo_chapter(source) == 1 for key, source in main.discover_demos().items() if "/" in key))

if __name__ == "__main__":
    unittest.main()
