"""Regression tests for native demo success/failure classification."""
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import main


def result(stdout="", stderr="", code=0):
    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=code)


class DemoCompletionTests(unittest.TestCase):
    def test_success_marker_on_own_line(self):
        self.assertTrue(main.demo_execution_succeeded(result("SDK output\nQGF_DEMO_OK\n")))

    def test_missing_marker(self):
        self.assertFalse(main.demo_execution_succeeded(result("Done\n")))

    def test_marker_embedded_in_other_text(self):
        self.assertFalse(main.demo_execution_succeeded(result("print(QGF_DEMO_OK)\n")))

    def test_nonzero_exit_with_marker(self):
        self.assertFalse(main.demo_execution_succeeded(result("QGF_DEMO_OK\n", code=1)))

    def test_semantic_error_even_with_marker(self):
        self.assertFalse(main.demo_execution_succeeded(result("Semantic error: wrong f32\nQGF_DEMO_OK\n")))

    def test_stderr_diagnostic_even_with_marker(self):
        self.assertFalse(main.demo_execution_succeeded(result("QGF_DEMO_OK\n", "Runtime error: failed")))

    def test_exception_even_with_marker(self):
        self.assertFalse(main.demo_execution_succeeded(result("QGF_DEMO_OK\n", "Traceback (most recent call last):")))

    def test_empty_streams(self):
        self.assertFalse(main.demo_execution_succeeded(result()))


if __name__ == "__main__":
    unittest.main()
