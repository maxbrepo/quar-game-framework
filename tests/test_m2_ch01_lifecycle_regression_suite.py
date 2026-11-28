"""Run the previously validated Chapter 1 lifecycle/SDL3 checkpoints together.

This runner only orchestrates existing tests; it does not copy lifecycle
logic, Visual Quar programs, or SDK bindings.
"""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CASES = (
    ("CP08", "test_m2_ch01_sdl3_contract_integration_runtime.py"),
    ("CP09", "test_m2_ch01_sdl3_error_recovery_runtime.py"),
    ("CP10", "test_m2_ch01_sdl3_native_failure_runtime.py"),
    ("CP11", "test_m2_ch01_lifecycle_contract_matrix_qrvm.py"),
    ("CP12", "test_m2_ch01_sdl3_guarded_cycles_runtime.py"),
)


def main():
    parser = argparse.ArgumentParser(description="QGF Chapter 1 lifecycle regression")
    parser.add_argument("--stop-on-failure", action="store_true")
    args = parser.parse_args()
    missing = [name for _, name in CASES if not (ROOT / "tests" / name).is_file()]
    if missing:
        print("BLOCKED: missing checkpoint tests:")
        for name in missing:
            print("  " + name)
        print("Apply the corresponding incremental checkpoint archives first.")
        return 2
    failed = []
    for checkpoint, filename in CASES:
        print("RUN:", checkpoint, filename, flush=True)
        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / "tests" / filename)],
                cwd=ROOT, timeout=90,
            )
            code = result.returncode
        except subprocess.TimeoutExpired:
            code = 124
            print("TIMEOUT:", checkpoint, flush=True)
        if code != 0:
            failed.append((checkpoint, code))
            print("FAIL:", checkpoint, "exit", code, flush=True)
            if args.stop_on_failure:
                break
        else:
            print("PASS:", checkpoint, flush=True)
    if failed:
        print("FAIL: Chapter 1 lifecycle regression:", failed)
        return 1
    print("PASS: Chapter 1 lifecycle regression 5/5 checkpoints (CP08-CP12)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
