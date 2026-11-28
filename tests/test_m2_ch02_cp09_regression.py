from pathlib import Path
import os
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import main
from test_ch02_pause_render_independence import *
for name, function in list(globals().items()):
    if name.startswith("test_") and callable(function):
        function()
subprocess.run([sys.executable, str(ROOT / "tests/test_m2_ch02_cp08_regression.py")], cwd=ROOT, check=True)
os.environ["SDL_VIDEODRIVER"] = "dummy"
keys = [key for key, path in main.discover_demos().items() if path.parent.name == "009_pause_render_independence"]
if not keys or main.run_demo(keys[0], ROOT / "sdk", smoke=True) is not True:
    sys.exit(1)
print("PASS: CP09 persistent Core and pause/render demo")
