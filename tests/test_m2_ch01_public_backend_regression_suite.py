"""Regression suite for public backend contract and verified SDL3 prepare."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CASES = (
    ("CP23", "test_m2_ch01_platform_state_matrix_qrvm.py"),
    ("CP24", "test_m2_ch01_platform_verified_native_runtime.py"),
    ("CP25", "test_m2_ch01_platform_verified_edges_qrvm.py"),
)


def main():
    missing = [filename for _, filename in CASES if not (ROOT / "tests" / filename).is_file()]
    if missing:
        print("BLOCKED: missing tests:", ", ".join(missing))
        return 2
    failures = []
    for checkpoint, filename in CASES:
        print("RUN:", checkpoint, flush=True)
        try:
            code = subprocess.run(
                [sys.executable, str(ROOT / "tests" / filename)],
                cwd=ROOT, timeout=120,
            ).returncode
        except subprocess.TimeoutExpired:
            code = 124
        if code:
            print("FAIL:", checkpoint, "exit", code, flush=True)
            failures.append(checkpoint)
        else:
            print("PASS:", checkpoint, flush=True)
    if failures:
        print("FAIL: public backend regression:", ", ".join(failures))
        return 1
    print("PASS: public backend regression 3/3 (CP23-CP25)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
