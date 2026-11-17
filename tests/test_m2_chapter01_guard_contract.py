"""Static contract checks only; not QRVM or SDL3 integration tests."""
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / 'experimental/marathon2/chapter01/qgf_lifecycle_guard.vq'


class GuardContract(unittest.TestCase):
    def test_source_exists(self):
        self.assertTrue(SOURCE.is_file())

    def test_canonical_entry_points(self):
        content = SOURCE.read_text(encoding='utf-8')
        for name in ('qgf_lifecycle_action_allowed', 'qgf_lifecycle_guarded_result', 'qgf_lifecycle_retry_requires_reset'):
            with self.subTest(name=name):
                self.assertIn(name + '(', content)

    def test_no_native_binding_duplication(self):
        content = SOURCE.read_text(encoding='utf-8')
        self.assertNotIn('extern "C"', content)
        self.assertNotIn('SDL_Init(', content)
        self.assertNotIn('SDL_Quit(', content)

    def test_invalid_actions_are_rejected(self):
        content = SOURCE.read_text(encoding='utf-8')
        self.assertIn('if (state < 0) { return false; }', content)
        self.assertIn('if (state > 2) { return false; }', content)
        self.assertIn('return false;', content)


if __name__ == '__main__':
    unittest.main()
