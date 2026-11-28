"""CP30 native lifecycle regression plus CP31 session entry/release guards."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TESTS = (
    "test_m2_ch01_session_cp30_regression.py",
    "test_m2_ch01_session_entry_release_qrvm.py",
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
    print("PASS: QGF Core session regression CP23-CP31 (9/9)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
