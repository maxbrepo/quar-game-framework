"""Experimental QRVM -> SDL3 driver name probe; does not initialize video."""
import argparse
import ctypes.util
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experimental/marathon2/chapter02/qgf_video_driver_probe.vq'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sdk', required=True, type=Path)
    parser.add_argument('--library', type=Path)
    args = parser.parse_args()
    sdk = args.sdk.expanduser().resolve()
    if not (sdk / 'main.py').is_file() or not SOURCE.is_file():
        print('BLOCKED: SDK or probe source missing')
        return 2
    if args.library:
        library = args.library.expanduser().resolve()
    else:
        name = ctypes.util.find_library('SDL3')
        library = next((p.resolve() for folder in (
            '/lib/x86_64-linux-gnu', '/usr/lib/x86_64-linux-gnu',
            '/lib/aarch64-linux-gnu', '/usr/lib/aarch64-linux-gnu',
            '/usr/local/lib', '/usr/local/lib64', '/lib', '/usr/lib')
            if name for p in [Path(folder) / name] if p.is_file()), None)
    if not library or not library.is_file():
        print('BLOCKED: SDL3 library unavailable')
        return 2
    try:
        result = subprocess.run(
            [sys.executable, str(sdk / 'main.py'), '--native-library',
             str(library), '-f', str(SOURCE)], input='1\n', text=True,
            capture_output=True, cwd=sdk, timeout=45)
    except subprocess.TimeoutExpired:
        print('FAIL: QRVM timeout')
        return 1
    if result.returncode or 'Program executed successfully' not in result.stdout:
        print('FAIL: QRVM/SDL3 video driver probe')
        print(result.stdout)
        print(result.stderr)
        return 1
    payload = result.stdout.split('=== QRVM OUTPUT ===', 1)[-1]
    lines = [line.strip() for line in payload.splitlines()
             if line.strip() and 'Program executed successfully' not in line]
    if not lines or not lines[0].isdigit():
        print('FAIL: missing driver count')
        print(result.stdout)
        return 1
    count = int(lines[0])
    if count < 0:
        print('FAIL: negative driver count')
        return 1
    print('PASS: SDL3 video driver count:', count)
    return 0


if __name__ == '__main__':
    sys.exit(main())
