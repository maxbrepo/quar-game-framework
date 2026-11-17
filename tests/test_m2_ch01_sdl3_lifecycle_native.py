"""Exercise real SDL3 state inspection and shutdown through external QRVM."""
from __future__ import annotations
import argparse
import ctypes.util
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experimental/marathon2/chapter01/qgf_sdl3_lifecycle_native_probe.vq'

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--sdk', required=True, type=Path)
    parser.add_argument('--library', type=Path)
    args = parser.parse_args()
    sdk = args.sdk.resolve()
    if not (sdk / 'main.py').is_file():
        print('BLOCKED: SDK main.py not found')
        return 2
    library = args.library.resolve() if args.library else None
    if library is None:
        name = ctypes.util.find_library('SDL3')
        if name:
            for directory in ('/lib/x86_64-linux-gnu', '/usr/lib/x86_64-linux-gnu', '/lib/aarch64-linux-gnu', '/usr/lib/aarch64-linux-gnu', '/usr/local/lib', '/usr/local/lib64', '/lib64', '/usr/lib64', '/lib', '/usr/lib'):
                candidate = Path(directory) / name
                if candidate.is_file():
                    library = candidate.resolve()
                    break
    if library is None or not library.is_file():
        print('BLOCKED: SDL3 library not found; use --library /absolute/path/to/libSDL3.so')
        return 2
    try:
        proc = subprocess.run(
            [sys.executable, str(sdk / 'main.py'), '--native-library', str(library), '-f', str(SOURCE)],
            input='1\n', text=True, capture_output=True, cwd=sdk, timeout=45)
    except subprocess.TimeoutExpired:
        print('FAIL: QRVM timeout')
        return 1
    if proc.returncode != 0 or '=== QRVM OUTPUT ===' not in proc.stdout or 'Program executed successfully' not in proc.stdout:
        print('FAIL: native SDL3 lifecycle probe did not complete')
        print(proc.stdout, proc.stderr)
        return 1
    output = proc.stdout.split('=== QRVM OUTPUT ===', 1)[1].split('Program executed successfully', 1)[0]
    numbers = [int(line.strip()) for line in output.splitlines() if line.strip().isdecimal()]
    if len(numbers) == 2 and numbers[1] == 0:
        print('PASS: SDL_WasInit(u32) -> SDL_Quit(void) -> SDL_WasInit(u32)')
        print('Video flags before:', numbers[0], 'after:', numbers[1])
        print('NOTE: SDL_Init not invoked; full initialization remains UNTESTED')
        return 0
    print('FAIL: unexpected SDL3 state output:', repr(output))
    return 1

if __name__ == '__main__':
    sys.exit(main())
