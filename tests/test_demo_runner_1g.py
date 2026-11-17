"""Regression checks for release-aware demo discovery and SDK validation."""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import main


class Runner1GTests(unittest.TestCase):
    def test_legacy_migrations_not_duplicated(self):
        demos = main.discover_demos()
        self.assertIn("0.0.1/01_core/001_hello_pixels", demos)
        self.assertIn("d001_hello_pixels", demos)
        self.assertEqual(main.resolve_demo("001_hello_pixels", demos), "0.0.1/01_core/001_hello_pixels")

    def test_missing_sdk_is_a_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(main, "find_sdl3_library", return_value="/tmp/libSDL3.so"):
                self.assertIs(main.run_demo("001_hello_pixels", Path(directory), smoke=True), False)

    def test_ambiguous_release_alias_is_rejected(self):
        demos = {"0.0.1/01_core/001_test": None, "0.0.2/01_core/001_test": None}
        self.assertIsNone(main.resolve_demo("001_test", demos))
        self.assertEqual(main.resolve_demo("0.0.2/01_core/001_test", demos), "0.0.2/01_core/001_test")

    def test_existing_demos_have_unique_canonical_ids(self):
        demos = main.discover_demos()
        self.assertGreaterEqual(len(demos), 7)
        self.assertEqual(len(demos), len(set(demos)))


if __name__ == "__main__":
    unittest.main()
