"""Regression tests for SDL3 demo discovery and bounded batch execution."""
import unittest
from pathlib import Path
from unittest.mock import patch
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import main


class DemoBatchTests(unittest.TestCase):
    def test_demo_discovery_and_chapter(self):
        demos = main.discover_demos()
        self.assertIn('d001_hello_pixels', demos)
        self.assertEqual(main.demo_chapter(demos['d001_hello_pixels']), 1)

    def test_batch_reports_success(self):
        with patch.object(main, 'run_demo', return_value=True) as run:
            self.assertTrue(main.run_demo_batch(Path('/tmp'), chapter=1))
            run.assert_called_once()

    def test_missing_sdl3_is_skip(self):
        with patch.object(main, 'find_sdl3_library', return_value=None):
            self.assertIsNone(main.run_demo('d001_hello_pixels', Path('/tmp'), smoke=True))

    def test_batch_skips_are_not_passes(self):
        with patch.object(main, 'run_demo', return_value=None):
            self.assertFalse(main.run_demo_batch(Path('/tmp'), chapter=1))


if __name__ == '__main__':
    unittest.main()
