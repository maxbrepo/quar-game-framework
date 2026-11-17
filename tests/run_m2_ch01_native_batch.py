"""Run Chapter 1 native checks as a batch against an external SDK."""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TESTS = (
    'test_m2_ch01_sdk_ffi_capabilities.py',
    'test_m2_ch01_ffi_i32_runtime.py',
    'test_m2_ch01_sdl3_version_runtime.py',
    'test_m2_ch01_sdl3_lifecycle_native.py',
)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--sdk', type=Path, required=True)
    parser.add_argument('--library', type=Path)
    args = parser.parse_args()
    sdk = args.sdk.resolve()
    if not (sdk / 'main.py').is_file():
        print('BLOCKED: external SDK main.py missing')
        return 2
    results = []
    for name in TESTS:
        script = ROOT / 'tests' / name
        if not script.is_file():
            print(f'BLOCKED: {name} is missing; install previous checkpoint')
            results.append((name, 'BLOCKED'))
            continue
        command = [sys.executable, str(script), '--sdk', str(sdk)]
        if args.library and name in TESTS[2:]:
            command.extend(('--library', str(args.library.resolve())))
        print(f'\n=== {name} ===', flush=True)
        try:
            result = subprocess.run(command, cwd=ROOT, capture_output=True,
                                    text=True, timeout=90)
        except subprocess.TimeoutExpired:
            print('FAIL: timeout')
            results.append((name, 'FAIL'))
            continue
        print(result.stdout, end='')
        if result.stderr:
            print(result.stderr, file=sys.stderr, end='')
        # Audit scripts may exit successfully even when reporting a known limitation.
        status = ('BLOCKED' if result.returncode == 2 else
                  'PASS' if result.returncode == 0 and 'FAIL:' not in result.stdout else
                  'FAIL')
        results.append((name, status))
    print('\n=== SUMMARY ===')
    for name, status in results:
        print(f'{status}: {name}')
    return 1 if any(status == 'FAIL' for _, status in results) else (
        2 if any(status == 'BLOCKED' for _, status in results) else 0)

if __name__ == '__main__':
    sys.exit(main())
