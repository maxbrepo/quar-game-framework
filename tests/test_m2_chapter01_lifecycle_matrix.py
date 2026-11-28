"""Chapter 1 lifecycle matrix: Python bootstrap behavior only, not QRVM/SDL3."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core import CoreError, CoreErrorCode, CoreState, QGFCore


class LifecycleMatrixTests(unittest.TestCase):
    def make_core(self, state):
        core = QGFCore()
        if state in (CoreState.INITIALIZED, CoreState.RUNNING, CoreState.STOPPED):
            core.initialize()
        if state is CoreState.RUNNING:
            core.start()
        if state is CoreState.STOPPED:
            core.stop()
        return core

    def test_all_state_operation_pairs(self):
        expected = {
            CoreState.CREATED: {"initialize": CoreState.INITIALIZED},
            CoreState.INITIALIZED: {"start": CoreState.RUNNING, "stop": CoreState.STOPPED},
            CoreState.RUNNING: {"stop": CoreState.STOPPED},
            CoreState.STOPPED: {},
        }
        for source, allowed in expected.items():
            for action in ("initialize", "start", "stop"):
                with self.subTest(source=source.name, action=action):
                    core = self.make_core(source)
                    before = core.status()
                    if action in allowed:
                        getattr(core, action)()
                        self.assertIs(core.state, allowed[action])
                        self.assertIsNone(core.status().last_error)
                    else:
                        with self.assertRaises(CoreError) as raised:
                            getattr(core, action)()
                        self.assertIs(core.state, source)
                        self.assertIs(raised.exception.code, CoreErrorCode.INVALID_TRANSITION)
                        self.assertIs(raised.exception.source, source)
                        self.assertIs(raised.exception.target, {
                            "initialize": CoreState.INITIALIZED,
                            "start": CoreState.RUNNING,
                            "stop": CoreState.STOPPED,
                        }[action])
                        self.assertIsNone(before.last_error)
                        self.assertIs(core.status().last_error, CoreErrorCode.INVALID_TRANSITION)

    def test_failed_operation_does_not_change_active_flag(self):
        for state in CoreState:
            for action in ("initialize", "start", "stop"):
                core = self.make_core(state)
                was_active = core.status().is_active
                try:
                    getattr(core, action)()
                except CoreError:
                    self.assertEqual(core.status().is_active, was_active)

    def test_snapshot_does_not_mutate_after_error(self):
        core = QGFCore()
        snapshot = core.status()
        with self.assertRaises(CoreError):
            core.stop()
        self.assertIs(snapshot.state, CoreState.CREATED)
        self.assertIsNone(snapshot.last_error)
        self.assertIs(core.status().last_error, CoreErrorCode.INVALID_TRANSITION)


if __name__ == "__main__":
    unittest.main()
