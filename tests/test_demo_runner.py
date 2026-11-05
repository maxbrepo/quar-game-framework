"""Check demo discovery without opening a graphical window."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import main

class DemoRunnerTests(unittest.TestCase):
    def test_demo_discovery_is_separate_from_examples(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            demo = root / "demos" / "hello_window" / "main.vq"
            demo.parent.mkdir(parents=True)
            demo.write_text("print(1);\n")
            with patch.object(main, "ROOT", root):
                self.assertEqual(main.discover_demos(), {"hello_window": demo})
                self.assertEqual(main.discover_examples(), {})

    def test_missing_demo_is_rejected(self):
        with TemporaryDirectory() as directory:
            with patch.object(main, "ROOT", Path(directory)):
                self.assertFalse(main.run_demo("missing", Path(directory)))
