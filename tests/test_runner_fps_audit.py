"""Regression checks for the non-executing FPS compatibility audit."""
import contextlib
import io
import unittest
import main


class FPSAuditTests(unittest.TestCase):
    def test_chapter_two_audit_does_not_execute_demos(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertTrue(main.audit_demo_fps(chapter=2))
        report = output.getvalue()
        self.assertIn("SUPPORTED=5 UNSUPPORTED=2", report)
        self.assertIn("Structural check only", report)


if __name__ == "__main__":
    unittest.main()
