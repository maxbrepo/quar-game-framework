"""Regression checks for cancellable child processes and menu separators."""
import contextlib
import importlib.util
import io
from pathlib import Path
import sys
import unittest

RUNNER = Path(__file__).resolve().parents[1] / 'main.py'
spec = importlib.util.spec_from_file_location('qgf_runner_1l', RUNNER)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class RunnerEscapeTests(unittest.TestCase):
    def test_process_output_and_exit_code(self):
        result = runner.interruptible_run(
            [sys.executable, '-c', 'print("OK")'], cwd=RUNNER.parent, timeout=5)
        self.assertEqual(result.returncode, 0)
        self.assertIn('OK', result.stdout)

    def test_timeout(self):
        import subprocess
        with self.assertRaises(subprocess.TimeoutExpired):
            runner.interruptible_run(
                [sys.executable, '-c', 'import time; time.sleep(5)'],
                cwd=RUNNER.parent, timeout=0.15)

    def test_main_menu_separator(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            runner.screen('QUAR GAME FRAMEWORK / 0.0.1', [(7, 'Run chapter'), (8, '2D graphical demos')])
        self.assertIn('-' * 46 + '\n[8]', output.getvalue())

    def test_demo_menu_separator(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            runner.screen('QGF - 2D DEMOS', [(1, 'Run one interactive demo'), (2, 'Batch all')])
        self.assertIn('-' * 46 + '\n[2]', output.getvalue())


if __name__ == '__main__':
    unittest.main()
