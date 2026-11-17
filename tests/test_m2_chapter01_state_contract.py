"""Static checks only; these are not QRVM or SDL3 execution tests."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "experimental/marathon2/chapter01/qgf_lifecycle_state.vq"

class LifecycleStateContract(unittest.TestCase):
    def test_state_functions_present(self):
        src = STATE.read_text(encoding="utf-8")
        for name in (
            "qgf_lifecycle_after_init", "qgf_lifecycle_can_init",
            "qgf_lifecycle_needs_shutdown", "qgf_lifecycle_after_shutdown",
            "qgf_lifecycle_can_reset_error", "qgf_lifecycle_after_error_reset",
            "qgf_lifecycle_can_restart",
        ):
            with self.subTest(name=name):
                self.assertIn(name + "(", src)

    def test_no_duplicate_native_bindings(self):
        src = STATE.read_text(encoding="utf-8")
        self.assertNotIn('extern "C"', src)
        self.assertNotIn("SDL_", src)
        self.assertNotIn("ctypes", src)

    def test_no_mutation_of_sdk(self):
        self.assertFalse((ROOT / "sdk").exists())

if __name__ == "__main__":
    unittest.main()
