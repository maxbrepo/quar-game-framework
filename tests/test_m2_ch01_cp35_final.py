from pathlib import Path
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[1]
for name in ("test_m2_ch01_session_cp33_regression.py", "test_m2_ch01_silent_session_final.py"):
    result = subprocess.run([sys.executable, str(ROOT / "tests" / name)], cwd=ROOT, timeout=600)
    if result.returncode:
        sys.exit(result.returncode)
print("PASS: Chapter 1 final regression (CP23-CP35)")
