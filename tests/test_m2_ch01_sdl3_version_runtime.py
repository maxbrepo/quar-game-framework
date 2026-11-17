"""Run SDL3 SDL_GetVersion through Visual Quar -> QRVM -> native FFI."""
from __future__ import annotations

import argparse
import ctypes.util
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experimental/marathon2/chapter01/qgf_sdl3_version_probe.vq'


def locate_sdl3(explicit: Path | None) -> Path | None:
    if explicit is not None:
        return explicit.expanduser().resolve()
    name = ctypes.util.find_library('SDL3')
    if not name:
        return None
    candidates = [
        Path(folder) / name for folder in (
            '/lib/x86_64-linux-gnu', '/usr/lib/x86_64-linux-gnu',
            '/lib/aarch64-linux-gnu', '/usr/lib/aarch64-linux-gnu',
            '/usr/local/lib', '/usr/local/lib64', '/lib64', '/usr/lib64',
            '/lib', '/usr/lib',
        )
    ]
    return next((candidate.resolve() for candidate in candidates if candidate.is_file()), None)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--sdk', required=True, type=Path)
    parser.add_argument('--library', type=Path, help='Absolute path to libSDL3.so')
    args = parser.parse_args()
    sdk = args.sdk.expanduser().resolve()
    if not (sdk / 'main.py').is_file():
        print('BLOCKED: SDK main.py not found')
        return 2
    if not SOURCE.is_file():
        print('BLOCKED: SDL3 Visual Quar probe missing')
        return 2
    library = locate_sdl3(args.library)
    if library is None or not library.is_file():
        print('BLOCKED: SDL3 library not found; use --library /absolute/path/to/libSDL3.so')
        return 2
    try:
        result = subprocess.run(
            [sys.executable, str(sdk / 'main.py'), '--native-library', str(library),
             '-f', str(SOURCE)], input='1\n', text=True, capture_output=True,
            cwd=sdk, timeout=45,
        )
    except subprocess.TimeoutExpired:
        print('FAIL: QRVM timed out')
        return 1
    output = result.stdout
    if result.returncode != 0 or '=== QRVM OUTPUT ===' not in output:
        print('FAIL: Visual Quar / QRVM native call failed')
        print(output)
        print(result.stderr)
        return 1
    payload = output.split('=== QRVM OUTPUT ===', 1)[1]
    lines = [line.strip() for line in payload.splitlines() if line.strip()]
    # SDL3 uses the packed major/minor/micro version integer (>= 3000000).
    values = [int(line) for line in lines if line.isdecimal()]
    if 'Program executed successfully' in payload and any(v >= 3000000 for v in values):
        print('PASS: VQ -> QRVM -> SDL3 SDL_GetVersion(i32)')
        print('SDL3 version integer:', next(v for v in values if v >= 3000000))
        return 0
    print('FAIL: expected SDL3 version integer >= 3000000')
    print(output)
    print(result.stderr)
    return 1


if __name__ == '__main__':
    sys.exit(main())
