"""Run cumulative public backend and session integration regressions."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CASES = (
    ("CP23", "test_m2_ch01_platform_state_matrix_qrvm.py"),
    ("CP24", "test_m2_ch01_platform_verified_native_runtime.py"),
    ("CP25", "test_m2_ch01_platform_verified_edges_qrvm.py"),
    ("CP26", "test_m2_ch01_platform_native_failure_core_qrvm.py"),
    ("CP27", "test_m2_ch01_app_backend_native_vertical.py"),
    ("CP28", "test_m2_ch01_session_native_coordination.py"),
    ("CP29", "test_m2_ch01_session_matrix_qrvm.py"),
)


def main():
    missing = [name for _, name in CASES if not (ROOT / "tests" / name).is_file()]
    if missing:
        print("BLOCKED: missing test files:", ", ".join(missing))
        return 2
    for checkpoint, name in CASES:
        print("RUN:", checkpoint, flush=True)
        try:
            result = subprocess.run([sys.executable, str(ROOT / "tests" / name)], cwd=ROOT, timeout=150)
        except subprocess.TimeoutExpired:
            print("FAIL:", checkpoint, "timeout")
            return 1
        if result.returncode:
            print("FAIL:", checkpoint, "exit", result.returncode)
            return 1
    print("PASS: Core backend + session regression 7/7 (CP23-CP29)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
