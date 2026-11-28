"""Check game loop transitions including invalid states."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SDK = Path(os.environ.get('QUAR_SDK', str(ROOT / 'sdk'))).resolve()

def main():
    core = '\n'.join(line for line in (ROOT / 'core/game_loop.vq').read_text().splitlines() if not line.lstrip().startswith('//'))
    lines = [core]
    expected = []
    for state in (-1, 0, 1, 2, 3, 4):
        cases = {
            'pause': 1 if state == 0 else state,
            'resume': 0 if state == 1 else state,
            'stop': 2 if state in (0, 1) else state,
            'finish': 3 if state == 2 else state,
        }
        for operation, value in cases.items():
            lines.append(f'print(qgf_loop_{operation}({state}));')
            expected.append(value)
        for operation, value in [('update', state == 0), ('render', state in (0, 1))]:
            lines.append(f'if (qgf_loop_can_{operation}({state})) {{ print(1); }} else {{ print(0); }}')
            expected.append(int(value))
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
    print(f'PASS: CP14 loop transition matrix {len(expected)}/{len(expected)}')
    return 0

if __name__ == '__main__':
    sys.exit(main())
