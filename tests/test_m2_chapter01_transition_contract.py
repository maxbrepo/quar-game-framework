"""Static contract checks, not Visual Quar runtime validation."""
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'experimental/marathon2/chapter01/qgf_lifecycle_transition.vq'
NATIVE = ROOT / 'experimental/marathon2/chapter01/qgf_lifecycle_native.vq'
class TransitionContract(unittest.TestCase):
    def test_transition_functions(self):
        source = SRC.read_text()
        for name in ('qgf_lifecycle_state_valid', 'qgf_lifecycle_init_requested',
                     'qgf_lifecycle_init_result', 'qgf_lifecycle_quit_requested',
                     'qgf_lifecycle_quit_result', 'qgf_lifecycle_reset_result',
                     'qgf_lifecycle_native_result_consistent'):
            with self.subTest(name=name): self.assertIn(name + '(', source)
    def test_no_native_binding_duplication(self):
        source = SRC.read_text()
        self.assertNotIn('extern "C"', source)
        self.assertNotIn('SDL_', source)
    def test_native_declarations_are_isolated(self):
        native = NATIVE.read_text()
        self.assertIn('extern "C" bool SDL_Init(u32 flags);', native)
        self.assertIn('extern "C" void SDL_Quit();', native)
    def test_no_sdk_copy(self):
        self.assertFalse((ROOT/'sdk').exists())
if __name__ == '__main__': unittest.main()
