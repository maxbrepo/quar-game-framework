"""Static contract tests; do not claim QRVM or SDL3 execution."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "experimental/marathon2/chapter01/qgf_lifecycle_sequence.vq"
TRANSITION = ROOT / "experimental/marathon2/chapter01/qgf_lifecycle_transition.vq"

class SequenceContract(unittest.TestCase):
    def test_files_present(self):
        self.assertTrue(SRC.is_file())
        self.assertTrue(TRANSITION.is_file())

    def test_expected_entrypoints(self):
        src = SRC.read_text()
        for name in ("qgf_lifecycle_next_action", "qgf_lifecycle_apply_init", "qgf_lifecycle_apply_quit", "qgf_lifecycle_apply_reset", "qgf_lifecycle_sequence_consistent"):
            self.assertIn(name + "(", src)

    def test_reuses_transition_helpers(self):
        src = SRC.read_text()
        for name in ("qgf_lifecycle_init_result", "qgf_lifecycle_quit_result", "qgf_lifecycle_reset_result", "qgf_lifecycle_native_result_consistent"):
            self.assertIn(name + "(", src)
            self.assertNotIn("int " + name + "(", src)
            self.assertNotIn("bool " + name + "(", src)

    def test_no_duplicate_native_binding(self):
        src = SRC.read_text()
        self.assertNotIn('extern "C"', src)
        self.assertNotIn('SDL_Init(', src)
        self.assertNotIn('SDL_Quit(', src)

if __name__ == "__main__":
    unittest.main()
