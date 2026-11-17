"""Structural FPS selection and source pacing regression checks."""
import unittest
import main


class FPSRunnerTests(unittest.TestCase):
    def test_fps_options(self):
        self.assertEqual(main.parse_fps('default'), None)
        self.assertEqual(main.parse_fps('unlimited'), 0)
        for fps in (5, 10, 15, 30, 60, 90, 120, 144, 300):
            self.assertEqual(main.parse_fps(str(fps)), fps)

    def test_fps_does_not_change_frame_budget(self):
        demo = next(main.ROOT.glob('demos/**/001_delta_time_moving_line/main.vq'))
        original = demo.read_text(encoding='utf-8')
        modified = main.apply_fps_cap(original, 60)
        self.assertIn('u64 max_frames = 60;', modified)
        self.assertIn('qgf_frame_start_ms', modified)
        self.assertEqual(main.apply_fps_cap(original, None), original)

    def test_invalid_fps(self):
        for fps in ('abc', '-1', '10001'):
            with self.assertRaises(ValueError):
                main.parse_fps(fps)


if __name__ == '__main__':
    unittest.main()
