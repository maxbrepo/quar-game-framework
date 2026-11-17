"""SDL3 native timing/driver smoke test using the external Quar SDK."""
from __future__ import annotations
import argparse
import ctypes.util
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experimental/marathon2/chapter01/qgf_sdl3_runtime_metrics_probe.vq'

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--sdk', required=True, type=Path)
    parser.add_argument('--library', type=Path)
    args = parser.parse_args()
    sdk = args.sdk.resolve()
    if not (sdk / 'main.py').is_file():
        print('BLOCKED: external SDK main.py missing')
        return 2
    library = args.library.resolve() if args.library else None
    if library is None:
        name = ctypes.util.find_library('SDL3')
        if name:
            for directory in ('/lib/x86_64-linux-gnu', '/usr/lib/x86_64-linux-gnu',
                              '/lib/aarch64-linux-gnu', '/usr/lib/aarch64-linux-gnu',
                              '/usr/local/lib', '/usr/local/lib64', '/lib64',
                              '/usr/lib64', '/lib', '/usr/lib'):
                candidate = Path(directory) / name
                if candidate.is_file():
                    library = candidate.resolve()
                    break
    if library is None or not library.is_file():
        print('BLOCKED: SDL3 library not found; specify --library')
        return 2
    try:
        proc = subprocess.run(
            [sys.executable, str(sdk / 'main.py'), '--native-library', str(library),
             '-f', str(SOURCE)], input='1\n', text=True, capture_output=True,
            cwd=sdk, timeout=45)
    except subprocess.TimeoutExpired:
        print('FAIL: QRVM timeout')
        return 1
    if proc.returncode or '=== QRVM OUTPUT ===' not in proc.stdout or 'Program executed successfully' not in proc.stdout:
        print('FAIL: native metrics probe did not complete')
        print(proc.stdout, proc.stderr)
        return 1
    output = proc.stdout.split('=== QRVM OUTPUT ===', 1)[1].split('Program executed successfully', 1)[0]
    try:
        values = [int(line.strip()) for line in output.splitlines() if line.strip()]
    except ValueError:
        print('FAIL: nonnumeric output:', repr(output))
        return 1
    if len(values) != 6:
        print('FAIL: expected six numeric outputs:', repr(output))
        return 1
    ticks_before, counter_before, frequency, drivers, counter_after, ticks_after = values
    if not (ticks_after >= ticks_before >= 0 and counter_after >= counter_before >= 0 and frequency > 0 and drivers >= 0):
        print('FAIL: inconsistent native metrics:', values)
        return 1
    print('PASS: SDL3 ticks, performance counter/frequency and video-driver count')
    print('Ticks:', ticks_before, '->', ticks_after)
    print('Performance counter:', counter_before, '->', counter_after)
    print('Frequency:', frequency, 'Video drivers:', drivers)
    print('NOTE: SDL_Init remains UNTESTED')
    return 0

if __name__ == '__main__':
    sys.exit(main())
