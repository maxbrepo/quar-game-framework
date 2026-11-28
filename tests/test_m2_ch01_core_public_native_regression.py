"""Grouped native SDL3 success/failure and public Core regression tests."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TESTS = (
    ("CP23", "test_m2_ch01_platform_state_matrix_qrvm.py"),
    ("CP24", "test_m2_ch01_platform_verified_native_runtime.py"),
    ("CP25", "test_m2_ch01_platform_verified_edges_qrvm.py"),
    ("CP26", "test_m2_ch01_platform_native_failure_core_qrvm.py"),
)


def main():
    missing = [name for _, name in TESTS if not (ROOT / "tests" / name).is_file()]
    if missing:
        print("BLOCKED: missing test files:", ", ".join(missing))
        return 2
    for checkpoint, filename in TESTS:
        print("RUN:", checkpoint, flush=True)
        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / "tests" / filename)],
                cwd=ROOT, timeout=120,
            )
        except subprocess.TimeoutExpired:
            print("FAIL:", checkpoint, "timeout")
            return 1
        if result.returncode:
            print("FAIL:", checkpoint, "exit", result.returncode)
            return 1
        print("PASS:", checkpoint, flush=True)
    print("PASS: Core public/native regression 4/4 (CP23-CP26)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
