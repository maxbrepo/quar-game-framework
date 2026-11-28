"""Grouped Chapter 1 edge-case regression, using existing tests."""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CASES = (
    ("CP17", "test_m2_ch01_sdl3_app_failure_guard_runtime.py"),
    ("CP18", "test_m2_ch01_sdl3_two_app_sessions_runtime.py"),
    ("CP19", "test_m2_ch01_sdl3_initialized_stop_runtime.py"),
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stop-on-failure", action="store_true")
    args = parser.parse_args()
    missing = [filename for _, filename in CASES if not (ROOT / "tests" / filename).is_file()]
    if missing:
        print("BLOCKED: missing tests:", ", ".join(missing))
        return 2
    failures = []
    for label, filename in CASES:
        print("RUN:", label, flush=True)
        try:
            code = subprocess.run(
                [sys.executable, str(ROOT / "tests" / filename)],
                cwd=ROOT, timeout=120,
            ).returncode
        except subprocess.TimeoutExpired:
            code = 124
        if code:
            print("FAIL:", label, "exit", code, flush=True)
            failures.append(label)
            if args.stop_on_failure:
                break
        else:
            print("PASS:", label, flush=True)
    if failures:
        print("FAIL: grouped lifecycle edge cases:", ", ".join(failures))
        return 1
    print("PASS: Chapter 1 edge cases 3/3 (CP17, CP18, CP19)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
