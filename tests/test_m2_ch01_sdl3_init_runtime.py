"""Runtime SDL3 initialization probe through the external Visual Quar SDK."""
from __future__ import annotations

import argparse
import ctypes.util
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "experimental/marathon2/chapter01/qgf_sdl3_init_bool_probe.vq"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sdk", type=Path, default=ROOT / "sdk")
    parser.add_argument("--library", type=Path, help="Path to the SDL3 shared library")
    args = parser.parse_args()
    sdk = args.sdk.resolve()
    if not (sdk / "main.py").is_file() or not SOURCE.is_file():
        print("BLOCKED: external SDK or QGF probe missing")
        return 2
    library = str(args.library.resolve()) if args.library else ctypes.util.find_library("SDL3")
    if not library:
        print("BLOCKED: SDL3 shared library unavailable")
        return 2
    env = os.environ.copy()
    env["SDL_VIDEODRIVER"] = "dummy"
    try:
        result = subprocess.run(
            [sys.executable, str(sdk / "main.py"), "--native-library", library,
             "-f", str(SOURCE)],
            input="1\n", text=True, capture_output=True, cwd=sdk,
            env=env, timeout=45,
        )
    except subprocess.TimeoutExpired:
        print("FAIL: QRVM SDL3 initialization timed out")
        return 1
    if result.returncode != 0 or "=== QRVM OUTPUT ===" not in result.stdout or "Program executed successfully" not in result.stdout:
        print("FAIL: QRVM did not complete the SDL3 initialization probe")
        print(result.stdout, result.stderr)
        return 1
    payload = result.stdout.split("=== QRVM OUTPUT ===", 1)[1].split("Program executed successfully", 1)[0]
    lines = [line.strip().lower() for line in payload.splitlines() if line.strip()]
    booleans = {"true": True, "false": False, "1": True, "0": False}
    first = next((booleans[line] for line in lines if line in booleans), None)
    if first is None:
        print("FAIL: missing SDL_Init boolean result:", repr(payload))
        return 1
    if not first:
        print("FAIL: SDL_Init returned false with SDL_VIDEODRIVER=dummy")
        return 1
    # Probe prints the SDL_Init result, SDL_WasInit before quit, and after quit.
    first_index = next(i for i, line in enumerate(lines) if line in booleans)
    values = [int(line) for line in lines[first_index + 1:] if line.isdecimal()]
    if len(values) < 2 or values[0] & 32 != 32 or values[1] != 0:
        print("FAIL: SDL_WasInit state invalid before/after SDL_Quit:", repr(payload))
        return 1
    print("PASS: SDL_Init(true) -> SDL_WasInit(video) -> SDL_Quit -> SDL_WasInit(0)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
