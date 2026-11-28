from pathlib import Path
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[1]
for name in ("test_m2_ch01_cp35_final.py", "test_m2_ch02_persistent_session.py"):
    result = subprocess.run([sys.executable, str(ROOT / "tests" / name)], cwd=ROOT)
    if result.returncode:
        sys.exit(result.returncode)
print("PASS: Chapter 1 regression and Chapter 2 persistent session")
