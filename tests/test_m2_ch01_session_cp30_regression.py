"""CP29 baseline and CP30 consecutive native session regression."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TESTS = (
    "test_m2_ch01_core_session_regression.py",
    "test_m2_ch01_session_two_native_cycles.py",
)


def main():
    for filename in TESTS:
        test = ROOT / "tests" / filename
        if not test.is_file():
            print("BLOCKED: missing", filename)
            return 2
        print("RUN:", filename, flush=True)
        try:
            result = subprocess.run([sys.executable, str(test)], cwd=ROOT, timeout=240)
        except subprocess.TimeoutExpired:
            print("FAIL: timeout", filename)
            return 1
        if result.returncode:
            print("FAIL:", filename, result.returncode)
            return 1
    print("PASS: QGF Core session cumulative regression CP23-CP30 (8/8)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
