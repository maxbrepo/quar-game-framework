"""Chapter 1 integrated lifecycle validation: existing checkpoints only."""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TESTS = (
    ("CP08", "test_m2_ch01_sdl3_contract_integration_runtime.py"),
    ("CP09", "test_m2_ch01_sdl3_error_recovery_runtime.py"),
    ("CP10", "test_m2_ch01_sdl3_native_failure_runtime.py"),
    ("CP11", "test_m2_ch01_lifecycle_contract_matrix_qrvm.py"),
    ("CP12", "test_m2_ch01_sdl3_guarded_cycles_runtime.py"),
    ("CP14", "test_m2_ch01_app_backend_lifecycle_contract_qrvm.py"),
    ("CP15", "test_m2_ch01_sdl3_app_backend_native_runtime.py"),
)


def main():
    parser = argparse.ArgumentParser(description="QGF Chapter 1 integrated lifecycle suite")
    parser.add_argument("--stop-on-failure", action="store_true")
    options = parser.parse_args()
    missing = [name for _, name in TESTS if not (ROOT / "tests" / name).is_file()]
    if missing:
        print("BLOCKED: missing tests:")
        for name in missing:
            print("  " + name)
        return 2
    failed = []
    for checkpoint, filename in TESTS:
        print("RUN:", checkpoint, flush=True)
        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / "tests" / filename)],
                cwd=ROOT, timeout=120,
            )
            code = result.returncode
        except subprocess.TimeoutExpired:
            code = 124
            print("TIMEOUT:", checkpoint, flush=True)
        if code:
            failed.append((checkpoint, code))
            print("FAIL:", checkpoint, "exit", code, flush=True)
            if options.stop_on_failure:
                break
        else:
            print("PASS:", checkpoint, flush=True)
    if failed:
        print("FAIL: Chapter 1 integrated lifecycle suite:", failed)
        return 1
    print("PASS: Chapter 1 integrated lifecycle suite 7/7 checkpoints (CP08-CP12, CP14-CP15)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
