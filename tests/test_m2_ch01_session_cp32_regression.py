"""Run the existing CP31 regression and the new reusable example."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TESTS = (
    "test_m2_ch01_session_cp31_regression.py",
    "test_m2_ch01_headless_sdl3_example.py",
)

def main():
    for name in TESTS:
        path = ROOT / "tests" / name
        if not path.is_file():
            print("BLOCKED: missing", name)
            return 2
        try:
            result = subprocess.run([sys.executable, str(path)], cwd=ROOT, timeout=240)
        except subprocess.TimeoutExpired:
            print("FAIL: timeout", name)
            return 1
        if result.returncode:
            print("FAIL:", name, result.returncode)
            return 1
    print("PASS: QGF Core regression and headless example CP23-CP32 (10/10)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
