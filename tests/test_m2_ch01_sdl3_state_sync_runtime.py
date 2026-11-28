"""Runtime check: QGF experimental backend state follows SDL3 initialization."""
import ctypes.util
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SDK = ROOT / "sdk"
SOURCE = ROOT / "experimental/marathon2/chapter01/qgf_sdl3_state_sync_probe.vq"


def main():
    if not (SDK / "main.py").is_file():
        print("BLOCKED: external Quar SDK missing")
        return 2
    library = ctypes.util.find_library("SDL3")
    if not library:
        print("BLOCKED: SDL3 library missing")
        return 2
    env = os.environ.copy()
    env["SDL_VIDEODRIVER"] = "dummy"
    try:
        result = subprocess.run(
            [sys.executable, str(SDK / "main.py"), "--native-library", library,
             "-f", str(SOURCE)],
            input="1\n", capture_output=True, text=True, cwd=SDK, env=env,
            timeout=45,
        )
    except subprocess.TimeoutExpired:
        print("FAIL: QRVM timed out")
        return 1
    if result.returncode != 0 or "=== QRVM OUTPUT ===" not in result.stdout or "Program executed successfully" not in result.stdout:
        print("FAIL: QRVM execution failed")
        print(result.stdout)
        print(result.stderr)
        return 1
    output = result.stdout.split("=== QRVM OUTPUT ===", 1)[1].split("Program executed successfully", 1)[0]
    values = [int(line.strip()) for line in output.splitlines() if line.strip().isdecimal()]
    expected_states = [1, 0, 1, 0]
    if len(values) != 8 or [values[i] for i in (0, 2, 4, 6)] != expected_states or values[3] != 0 or values[7] != 0 or (values[1] & 32) != 32 or (values[5] & 32) != 32:
        print("FAIL: inconsistent backend state / SDL3 state")
        print("Observed:", values)
        return 1
    print("PASS: backend state STOPPED -> ACTIVE -> STOPPED, repeated twice; SDL3 flags consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
