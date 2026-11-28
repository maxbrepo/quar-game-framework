"""Check deterministic movement across game loop states."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SDK = Path(os.environ.get("QUAR_SDK", str(ROOT / "sdk"))).resolve()

def main():
    paths = [ROOT / 'core/input.vq', ROOT / 'core/game_loop.vq', ROOT / 'examples/05 input system/076 directional movement/main.vq']
    lines = [line for path in paths for line in path.read_text().splitlines() if not line.lstrip().startswith('//')]
    expected = [1, -1, 1, -1, 2, -2, 2, -3, 1, -3, 1, -3, 1, -3]
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
    print(f'PASS: CP02 directional movement {len(expected)}/{len(expected)}')
    return 0

if __name__ == '__main__':
    sys.exit(main())
