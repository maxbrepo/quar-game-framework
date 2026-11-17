"""Run the experimental lifecycle logic through an external Visual Quar SDK."""
from pathlib import Path
import argparse
import os
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MODULES = ('qgf_lifecycle_state.vq', 'qgf_lifecycle_transition.vq',
           'qgf_lifecycle_guard.vq', 'qgf_lifecycle_sequence.vq',
           'qgf_lifecycle_contract.vq', 'qgf_lifecycle_qrvm_smoke.vq')
EXPECTED = ['1', '1', '2', '0', '2', '3', '0', 'false', 'true', 'false']

def main(sdk):
    if not (sdk / 'main.py').is_file():
        print('BLOCKED: SDK main.py not found')
        return 2
    folder = ROOT / 'experimental/marathon2/chapter01'
    sources = []
    for name in MODULES:
        path = folder / name
        if not path.is_file():
            print('BLOCKED: missing', path)
            return 2
        # Remove comments only in temporary test source for SDK lexer compatibility.
        sources.append('\n'.join(line for line in path.read_text().splitlines()
                                 if not line.lstrip().startswith('//')))
    with tempfile.TemporaryDirectory(prefix='qgf_m2_ch01_') as tmp:
        source = Path(tmp) / 'smoke.vq'
        source.write_text('\n'.join(sources) + '\n')
        try:
            result = subprocess.run([sys.executable, str(sdk / 'main.py'), '-f', str(source)],
                                    cwd=sdk, input='1\n', text=True, capture_output=True,
                                    timeout=45, env={**os.environ, 'TERM': 'dumb'})
        except subprocess.TimeoutExpired:
            print('FAIL: QRVM timeout')
            return 1
    if '=== QRVM OUTPUT ===' not in result.stdout or 'Program executed successfully' not in result.stdout:
        print('FAIL: QRVM did not execute', result.stdout, result.stderr)
        return 1
    output = result.stdout.split('=== QRVM OUTPUT ===', 1)[1].split('Program executed successfully', 1)[0]
    actual = [line.strip().lower() for line in output.splitlines() if line.strip()]
    print('Expected:', ', '.join(EXPECTED))
    print('Actual:  ', ', '.join(actual))
    print('PASS: 10/10 output assertions' if actual == EXPECTED else 'FAIL: unexpected output')
    return 0 if actual == EXPECTED else 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sdk', required=True, type=Path)
    args = parser.parse_args()
    sys.exit(main(args.sdk.expanduser().resolve()))
