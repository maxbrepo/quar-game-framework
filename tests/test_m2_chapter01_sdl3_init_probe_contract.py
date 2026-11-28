"""SDL3 initialization probe contract; no native runtime is simulated."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "experimental" / "marathon2" / "chapter01"


class SDL3InitProbeContract(unittest.TestCase):
    def test_real_native_bool_signature(self):
        source = (EXPERIMENT / "qgf_sdl3_init_bool_probe.vq").read_text(encoding="utf-8")
        self.assertIn('extern "C" bool SDL_Init(u32 flags);', source)
        self.assertIn('extern "C" u32 SDL_WasInit(u32 flags);', source)
        self.assertIn('extern "C" void SDL_Quit();', source)

    def test_success_only_enters_active_branch(self):
        source = (EXPERIMENT / "qgf_sdl3_init_bool_probe.vq").read_text(encoding="utf-8")
        self.assertIn('if (initialized) {', source)
        self.assertIn('SDL_Quit();', source)
        self.assertLess(source.index('if (initialized) {'), source.index('    SDL_Quit();'))

    def test_shutdown_observed_after_native_call(self):
        source = (EXPERIMENT / "qgf_sdl3_init_bool_probe.vq").read_text(encoding="utf-8")
        self.assertLess(source.index('    SDL_Quit();'), source.index('u32 after = SDL_WasInit(video_flags);'))
        self.assertIn('print(after);', source)

    def test_existing_runner_requires_external_sdk(self):
        runner = (ROOT / "tests" / "test_m2_ch01_sdl3_lifecycle_native.py").read_text(encoding="utf-8")
        self.assertIn("parser.add_argument('--sdk', required=True", runner)
        self.assertIn("parser.add_argument('--library'", runner)
        self.assertIn("'BLOCKED: SDL3 library not found", runner)
        self.assertIn("'NOTE: SDL_Init not invoked", runner)

    def test_no_local_ffi_adapter_or_sdk_mutation(self):
        source = (EXPERIMENT / "qgf_sdl3_init_bool_probe.vq").read_text(encoding="utf-8")
        self.assertNotIn('ctypes', source)
        self.assertNotIn('SDL_GetError', source)
        self.assertNotIn('SDL_CreateWindow', source)


if __name__ == "__main__":
    unittest.main()
