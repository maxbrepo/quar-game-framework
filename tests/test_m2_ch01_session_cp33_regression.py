"""Cumulative Core regression and success/failure tests of the same public example."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TESTS = (
    "test_m2_ch01_session_cp32_regression.py",
    "test_m2_ch01_headless_sdl3_failure.py",
)


def main():
    for filename in TESTS:
        path = ROOT / "tests" / filename
        if not path.is_file():
            print("BLOCKED: missing", filename)
            return 2
        try:
            result = subprocess.run([sys.executable, str(path)], cwd=ROOT, timeout=240)
        except subprocess.TimeoutExpired:
            print("FAIL: timeout", filename)
            return 1
        if result.returncode:
            print("FAIL:", filename, "exit", result.returncode)
            return 1
    print("PASS: QGF Core regression and headless success/failure CP23-CP33 (11/11)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
