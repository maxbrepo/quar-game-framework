"""Run the already validated QGF native probes against an external SDK."""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PROBES = (
    ('C i32 ABI', 'test_m2_ch01_ffi_i32_runtime.py'),
    ('SDL3 version', 'test_m2_ch01_sdl3_version_runtime.py'),
    ('SDL3 lifecycle query', 'test_m2_ch01_sdl3_lifecycle_native.py'),
    ('SDL3 metrics', 'test_m2_ch01_sdl3_runtime_metrics.py'),
)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sdk', type=Path, required=True)
    parser.add_argument('--library', type=Path)
    args = parser.parse_args()
    sdk = args.sdk.resolve()
    if not (sdk / 'main.py').is_file():
        print(f'BLOCKED: external SDK not found: {sdk}')
        return 2
    results = []
    for label, filename in PROBES:
        script = ROOT / 'tests' / filename
        if not script.is_file():
            print(f'BLOCKED: {label}: missing {script}')
            results.append((label, 'BLOCKED'))
            continue
        command = [sys.executable, str(script), '--sdk', str(sdk)]
        if args.library and label.startswith('SDL3'):
            command.extend(['--library', str(args.library.resolve())])
        print(f'\n=== {label} ===', flush=True)
        try:
            proc = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=90)
        except subprocess.TimeoutExpired:
            print('FAIL: timeout')
            results.append((label, 'FAIL'))
            continue
        print(proc.stdout, end='')
        if proc.stderr:
            print(proc.stderr, file=sys.stderr, end='')
        # Only mark PASS on an explicit PASS line, not just exit code zero.
        lines = [line.strip() for line in proc.stdout.splitlines()]
        if proc.returncode == 2 or any(line.startswith('BLOCKED:') for line in lines):
            status = 'BLOCKED'
        elif proc.returncode == 0 and any(line.startswith('PASS:') for line in lines) and not any(line.startswith('FAIL:') for line in lines):
            status = 'PASS'
        else:
            status = 'FAIL'
        results.append((label, status))
    print('\n=== QGF CH01 NATIVE BATCH SUMMARY ===')
    for label, status in results:
        print(f'{status}: {label}')
    print('UNTESTED: SDL_Init / full SDL3 initialization')
    if any(status == 'FAIL' for _, status in results):
        return 1
    if any(status == 'BLOCKED' for _, status in results):
        return 2
    return 0

if __name__ == '__main__':
    sys.exit(main())
