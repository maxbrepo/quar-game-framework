"""Regression tests for the Chapter 1A bootstrap lifecycle."""
import unittest
import sys
from pathlib import Path

# Allow direct execution by the QGF Main Runner from the tests directory.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from dataclasses import FrozenInstanceError
from core import CoreConfig, CoreError, CoreErrorCode, CoreState, QGFCore


class CoreLifecycleTests(unittest.TestCase):
    def test_status_snapshots_follow_lifecycle(self):
        core = QGFCore(CoreConfig("Sample"))
        created = core.status()
        self.assertEqual(created.app_name, "Sample")
        self.assertIs(created.state, CoreState.CREATED)
        self.assertFalse(created.is_active)
        core.initialize()
        self.assertIs(core.status().state, CoreState.INITIALIZED)
        core.start()
        self.assertTrue(core.status().is_active)
        core.stop()
        self.assertFalse(core.status().is_active)
        self.assertIs(created.state, CoreState.CREATED)

    def test_status_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            QGFCore().status().is_active = True

    def test_failed_transition_keeps_status_unchanged(self):
        core = QGFCore()
        before = core.status()
        with self.assertRaises(CoreError):
            core.start()
        self.assertEqual(core.state, before.state)
        self.assertIs(core.status().last_error, CoreErrorCode.INVALID_TRANSITION)

    def test_error_has_stable_code_and_context(self):
        core = QGFCore()
        with self.assertRaises(CoreError) as caught:
            core.start()
        self.assertIs(caught.exception.code, CoreErrorCode.INVALID_TRANSITION)
        self.assertIs(caught.exception.source, CoreState.CREATED)
        self.assertIs(caught.exception.target, CoreState.RUNNING)

    def test_last_error_is_none_before_failure(self):
        core = QGFCore()
        core.initialize()
        core.start()
        self.assertIsNone(core.status().last_error)

    def test_failure_does_not_prevent_valid_next_transition(self):
        core = QGFCore()
        with self.assertRaises(CoreError):
            core.start()
        core.initialize()
        core.start()
        self.assertIs(core.state, CoreState.RUNNING)
        self.assertIs(core.status().last_error, CoreErrorCode.INVALID_TRANSITION)

    def test_default_configuration(self):
        self.assertEqual(QGFCore().config.app_name, "QGF Application")

    def test_custom_configuration(self):
        self.assertEqual(QGFCore(CoreConfig("Demo")).config.app_name, "Demo")

    def test_invalid_name(self):
        for name in ("", "   ", None, 42):
            with self.subTest(name=name), self.assertRaises(ValueError):
                CoreConfig(name)

    def test_wrong_config_type(self):
        with self.assertRaises(TypeError):
            QGFCore("Demo")

    def test_initial_state(self):
        self.assertIs(QGFCore().state, CoreState.CREATED)

    def test_full_lifecycle(self):
        core = QGFCore()
        core.initialize()
        self.assertIs(core.state, CoreState.INITIALIZED)
        core.start()
        self.assertIs(core.state, CoreState.RUNNING)
        core.stop()
        self.assertIs(core.state, CoreState.STOPPED)

    def test_stop_after_initialize(self):
        core = QGFCore()
        core.initialize()
        core.stop()
        self.assertIs(core.state, CoreState.STOPPED)

    def test_cannot_start_before_initialize(self):
        core = QGFCore()
        with self.assertRaises(CoreError):
            core.start()
        self.assertIs(core.state, CoreState.CREATED)

    def test_cannot_stop_before_initialize(self):
        with self.assertRaises(CoreError):
            QGFCore().stop()

    def test_cannot_initialize_twice(self):
        core = QGFCore()
        core.initialize()
        with self.assertRaises(CoreError):
            core.initialize()

    def test_cannot_start_twice(self):
        core = QGFCore()
        core.initialize()
        core.start()
        with self.assertRaises(CoreError):
            core.start()

    def test_stopped_is_terminal(self):
        core = QGFCore()
        core.initialize()
        core.stop()
        for operation in (core.initialize, core.start, core.stop):
            with self.subTest(operation=operation.__name__), self.assertRaises(CoreError):
                operation()
        self.assertIs(core.state, CoreState.STOPPED)


if __name__ == "__main__":
    unittest.main()
