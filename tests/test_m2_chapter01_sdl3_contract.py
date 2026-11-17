"""Static safety checks for experimental SDL3 lifecycle integration."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "experimental/marathon2/chapter01/qgf_lifecycle_native.vq"

class TestSDL3LifecycleContract(unittest.TestCase):
    def test_sdl3_init_uses_bool_and_u32(self):
        self.assertIn('extern "C" bool SDL_Init(u32 flags);', EXPERIMENT.read_text())

    def test_no_unsupported_cstring_return(self):
        text = EXPERIMENT.read_text()
        self.assertNotIn('extern "C" const char* SDL_GetError', text)
        self.assertNotIn('extern "C" cstring SDL_GetError', text)

    def test_sdk_not_copied_into_experiment(self):
        text = EXPERIMENT.read_text()
        self.assertNotIn('ctypes', text)
        self.assertNotIn('SDL_CreateWindow', text)

    def test_production_lifecycle_unchanged_by_experiment(self):
        self.assertTrue((ROOT / 'core/lifecycle.vq').is_file())
        self.assertIn('qgf_can_initialize', (ROOT / 'core/lifecycle.vq').read_text())

if __name__ == '__main__':
    unittest.main()
