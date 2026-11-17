"""Execute the Visual Quar -> QRVM -> native C i32 smoke test."""
from __future__ import annotations
import argparse
import ctypes.util
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experimental/marathon2/chapter01/qgf_ffi_i32_abs_probe.vq'


def find_libc() -> Path | None:
    name = ctypes.util.find_library('c')
    if not name:
        return None
    candidates = [
        Path(folder) / name
        for folder in ('/lib/x86_64-linux-gnu', '/usr/lib/x86_64-linux-gnu',
                       '/lib/aarch64-linux-gnu', '/usr/lib/aarch64-linux-gnu',
                       '/lib64', '/usr/lib64', '/lib', '/usr/lib')
    ]
    return next((p.resolve() for p in candidates if p.is_file()), None)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--sdk', type=Path, required=True)
    parser.add_argument('--library', type=Path, help='Optional absolute path to libc shared library')
    args = parser.parse_args()
    sdk = args.sdk.expanduser().resolve()
    library = args.library.expanduser().resolve() if args.library else find_libc()
    if not (sdk / 'main.py').is_file():
        print('BLOCKED: SDK main.py missing')
        return 2
    if not SOURCE.is_file():
        print('BLOCKED: Visual Quar probe missing')
        return 2
    if library is None or not library.is_file():
        print('BLOCKED: libc not found; pass --library /absolute/path/to/libc.so.6')
        return 2
    try:
        result = subprocess.run(
            [sys.executable, str(sdk / 'main.py'), '--native-library', str(library),
             '-f', str(SOURCE)], input='1\n', capture_output=True, text=True,
            cwd=sdk, timeout=45,
        )
    except subprocess.TimeoutExpired:
        print('FAIL: QRVM timed out')
        return 1
    output = result.stdout
    if result.returncode != 0 or '=== QRVM OUTPUT ===' not in output:
        print('FAIL: QRVM did not reach native output')
        print(output)
        print(result.stderr)
        return 1
    payload = output.split('=== QRVM OUTPUT ===', 1)[1]
    lines = [line.strip() for line in payload.splitlines() if line.strip()]
    passed = '37' in lines and 'Program executed successfully' in payload
    print('PASS: VQ -> QRVM -> C abs(i32) returned 37' if passed else 'FAIL: expected 37')
    if not passed:
        print(output)
        print(result.stderr)
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())
