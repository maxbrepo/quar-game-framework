"""Check game action axis against independent state expectations."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SDK = Path(os.environ.get("QUAR_SDK", str(ROOT / "sdk"))).resolve()

def main():
    core = '\n'.join(line for line in (ROOT / 'core/input.vq').read_text().splitlines() if not line.lstrip().startswith('//'))
    lines = [core]
    expected = []
    for negative in (-1, 0, 1, 2, 3, 4):
        for positive in (-1, 0, 1, 2, 3, 4):
            lines.append(f'print(qgf_input_action_axis({negative}, {positive}));')
            expected.append(int(positive in (1, 2)) - int(negative in (1, 2)) if 0 <= negative <= 3 and 0 <= positive <= 3 else 0)
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / 'matrix.vq'
        source.write_text('\n'.join(lines))
        result = subprocess.run([sys.executable, str(SDK / 'main.py'), '-f', str(source)], cwd=SDK, input='1\n', text=True, capture_output=True, timeout=90)
    if result.returncode or '=== QRVM OUTPUT ===' not in result.stdout or 'Program executed successfully' not in result.stdout:
        print(result.stdout, result.stderr)
        return 1
    payload = result.stdout.split('=== QRVM OUTPUT ===', 1)[1].split('Program executed successfully', 1)[0]
    actual = [int(line.strip()) for line in payload.splitlines() if line.strip()]
    if actual != expected:
        print('FAIL:', actual, 'expected:', expected)
        return 1
    print(f'PASS: CP01 game action axis {len(expected)}/{len(expected)}')
    return 0

if __name__ == '__main__':
    sys.exit(main())
