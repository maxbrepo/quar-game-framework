"""Dependency-free regression tests for the QGF terminal runner."""
import contextlib
import importlib.util
import io
import subprocess
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

RUNNER = Path(__file__).resolve().parents[1] / 'main.py'
spec = importlib.util.spec_from_file_location('qgf_runner', RUNNER)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class QRVMSourceTests(unittest.TestCase):
    def test_comment_only_lines_are_removed(self):
        text = "// States: 0 CREATED\nint state() {\n    return 0;\n}\n"
        self.assertEqual(runner.qrvm_source(text), "\nint state() {\n    return 0;\n}\n")

    def test_non_comment_code_is_preserved(self):
        text = "print(3);\n    // Explanation: only\nprint(4);\n"
        self.assertEqual(runner.qrvm_source(text), "print(3);\n\nprint(4);\n")


class RunnerTests(unittest.TestCase):
    def test_unittest_detection(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "test_unit.py"
            source.write_text("import unittest\nclass T(unittest.TestCase):\n    pass\n", encoding="utf-8")
            self.assertEqual(runner.test_kind(source), "unittest")
            source.write_text("print('smoke')\n", encoding="utf-8")
            self.assertEqual(runner.test_kind(source), "sdk")

    def test_unit_runner_does_not_pass_sdk(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "test_unit.py"
            source.write_text("import unittest\nclass T(unittest.TestCase):\n    pass\n", encoding="utf-8")
            with patch.object(runner, "ROOT", root), patch.object(runner.subprocess, "run") as process:
                process.return_value.returncode = 0
                process.return_value.stdout = ""
                process.return_value.stderr = ""
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertTrue(runner.run_external_files(root, [source]))
                args = process.call_args.args[0]
                self.assertEqual(args[-1], "-v")
                self.assertNotIn("--sdk", args)

    def test_sdk_runner_receives_sdk(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "test_math.py"
            source.write_text("print('smoke')\n", encoding="utf-8")
            with patch.object(runner, "ROOT", root), patch.object(runner.subprocess, "run") as process:
                process.return_value.returncode = 0
                process.return_value.stdout = ""
                process.return_value.stderr = ""
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertTrue(runner.run_external_files(root, [source]))
                self.assertIn("--sdk", process.call_args.args[0])

    def test_discovery_prefers_categorized_layout(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for folder in ('examples/001_math', 'examples/01 core/001 vector2'):
                path = root / folder
                path.mkdir(parents=True)
                (path / 'main.vq').write_text('test', encoding='utf-8')
            with patch.object(runner, 'ROOT', root):
                self.assertEqual(runner.discover_examples()['001'].parent.name, '001 vector2')

    def test_only_existing_tests_discovered(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'tests').mkdir()
            (root / 'tests' / 'test_math.py').write_text('pass', encoding='utf-8')
            with patch.object(runner, 'ROOT', root):
                self.assertEqual([p.name for p in runner.discover_tests()], ['test_math.py'])

    def test_missing_module_is_unavailable(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / 'main.vq'
            source.write_text('test', encoding='utf-8')
            with patch.object(runner, 'ROOT', root):
                self.assertIn('missing module', runner.availability('001', source))

    def test_invalid_selection_then_back(self):
        with patch('builtins.input', side_effect=['bad', '0']):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(runner.select([(0, 'Back'), (1, 'Example')]), '0')
            self.assertIn('Invalid selection', output.getvalue())

    def test_main_exit(self):
        with patch.object(runner, 'screen'), patch.object(runner, 'clear_screen'):
            with patch('builtins.input', return_value='0'):
                self.assertEqual(runner.interactive(Path('/unused')), 0)

    def test_list_without_sdk(self):
        with patch('sys.argv', ['main.py', '--list', '--sdk', '/nonexistent']):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(runner.main(), 0)

    def test_check_reports_missing_dependency(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / 'examples' / '01 core' / '001 vector2'
            path.mkdir(parents=True)
            (path / 'main.vq').write_text('test', encoding='utf-8')
            with patch.object(runner, 'ROOT', root), patch('sys.argv', ['main.py', '--check']):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(runner.main(), 1)


class SummaryRegressionTests(unittest.TestCase):
    def test_examples_continue_after_failure_and_skip(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            examples = {"001": root / 'one.vq', "002": root / 'two.vq', "003": root / 'three.vq'}
            with patch.object(runner, 'discover_examples', return_value=examples), \
                 patch.object(runner, 'availability', side_effect=[None, 'missing module', None]), \
                 patch.object(runner, 'run_example', side_effect=[False, True]) as run:
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    self.assertFalse(runner.run_all(root))
                self.assertEqual(run.call_count, 2)
                self.assertIn('PASS=1 FAIL=1 SKIP=1 TOTAL=3', output.getvalue())

    def test_tests_continue_after_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            paths = [root / 'test_one.py', root / 'test_two.py']
            for path in paths:
                path.write_text('print(1)', encoding='utf-8')
            with patch.object(runner, 'ROOT', root), \
                 patch.object(runner.subprocess, 'run') as process:
                process.side_effect = [subprocess.CompletedProcess([], 1, '', ''),
                                       subprocess.CompletedProcess([], 0, '', '')]
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    self.assertFalse(runner.run_external_files(root, paths))
                self.assertEqual(process.call_count, 2)
                self.assertIn('PASS=1 FAIL=1 SKIP=0 TOTAL=2', output.getvalue())

    def test_missing_test_skips_without_crashing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertFalse(runner.run_external_files(root, [root / 'missing.py']))
            self.assertIn('SKIP=1', output.getvalue())


class ConsolidationTests(unittest.TestCase):
    def test_missing_sdk_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                runner.sdk_path(Path(temp))

    def test_skipped_example_does_not_count_as_full_success(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            examples = {"001": root / "one.vq", "002": root / "two.vq"}
            with patch.object(runner, "discover_examples", return_value=examples), \
                 patch.object(runner, "availability", side_effect=[None, "missing module"]), \
                 patch.object(runner, "run_example", return_value=True):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertFalse(runner.run_all(root))

    def test_skipped_test_does_not_count_as_full_success(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            good = root / "test_good.py"
            good.write_text("print('ok')", encoding="utf-8")
            with patch.object(runner, "ROOT", root), \
                 patch.object(runner.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "", "")):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertFalse(runner.run_external_files(root, [good, root / "missing.py"]))


if __name__ == '__main__':
    unittest.main()


class GameLoopDiscoveryTests(unittest.TestCase):
    def test_game_loop_dependency_is_registered(self):
        self.assertEqual(runner.MODULES.get("004"), "core/game_loop.vq")
        self.assertEqual(runner.EXPECTED.get("004"),
                         ["true", "false", "true", "false",
                          "true", "true", "false", "true"])


class FixedUpdateDiscoveryTests(unittest.TestCase):
    def test_fixed_update_example_registered(self):
        self.assertEqual(runner.MODULES.get("005"), "core/game_loop.vq")
        self.assertEqual(runner.EXPECTED.get("005"),
                         ["0", "1", "3", "2", "0", "0", "0", "5", "15", "0", "true"])


class RenderInterpolationDiscoveryTests(unittest.TestCase):
    def test_render_interpolation_example_registered(self):
        self.assertEqual(runner.MODULES.get("006"), "core/game_loop.vq")
        self.assertEqual(runner.EXPECTED.get("006"),
                         ["0.0", "0.25", "1.0", "0.0", "0.0",
                          "10.0", "20.0", "30.0", "10.0", "30.0"])


class GameLoopExecutionDiscoveryTests(unittest.TestCase):
    def test_game_loop_execution_example_registered(self):
        self.assertEqual(runner.MODULES.get("007"), "core/game_loop.vq")
        self.assertEqual(runner.EXPECTED.get("007"),
                         ["60", "2", "20", "1.0", "1", "5", "0.25", "5", "0"])
