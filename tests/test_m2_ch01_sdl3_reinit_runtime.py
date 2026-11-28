"""Verify two SDL3 init/quit cycles in a single QRVM execution."""
import ctypes.util
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SDK = ROOT / "sdk"
SOURCE = ROOT / "experimental/marathon2/chapter01/qgf_sdl3_reinit_probe.vq"


def main():
    if not (SDK / "main.py").is_file():
        print("BLOCKED: external SDK missing")
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
        print("FAIL: QRVM execution timed out")
        return 1
    if result.returncode or "=== QRVM OUTPUT ===" not in result.stdout or "Program executed successfully" not in result.stdout:
        print("FAIL: QRVM execution failed")
        print(result.stdout)
        print(result.stderr)
        return 1
    payload = result.stdout.split("=== QRVM OUTPUT ===", 1)[1].split("Program executed successfully", 1)[0]
    lines = [line.strip().lower() for line in payload.splitlines() if line.strip()]
    values = [line for line in lines if line in ("true", "false") or line.isdecimal()]
    expected = ["true", "32", "0", "true", "32", "0"]
    if len(values) != len(expected) or any(
        (actual not in ("true", "1") if target == "true" else
         (not actual.isdecimal() or (int(actual) & 32) != 32) if target == "32" else
         actual != "0")
        for actual, target in zip(values, expected)
    ):
        print("FAIL: expected two clean SDL3 video initialization cycles")
        print("Actual values:", values)
        return 1
    print("PASS: two consecutive SDL_Init -> SDL_WasInit -> SDL_Quit cycles")
    return 0


if __name__ == "__main__":
    sys.exit(main())
