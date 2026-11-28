"""Exercise the existing Core timing pipeline with deterministic timestamps."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SDK = Path(os.environ.get('QUAR_SDK', str(ROOT / 'sdk'))).resolve()
SOURCES = ('core/time.vq', 'core/game_loop.vq', 'experimental/marathon2/chapter02/qgf_integer_pacing_probe.vq')
EXPECTED = [11, 0, 0, 0, 0, 9, 0, 50, 10, 0, 2, 25, 2, 0, 60, 0, 16]

def main():
    program = '\n'.join(line for name in SOURCES for line in (ROOT / name).read_text().splitlines() if not line.lstrip().startswith('//'))
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / 'timing.vq'
        source.write_text(program)
        result = subprocess.run([sys.executable, str(SDK / 'main.py'), '-f', str(source)], cwd=SDK, input='1\n', text=True, capture_output=True, timeout=90)
    if result.returncode or '=== QRVM OUTPUT ===' not in result.stdout or 'Program executed successfully' not in result.stdout:
        print(result.stdout, result.stderr)
        return 1
    payload = result.stdout.split('=== QRVM OUTPUT ===', 1)[1].split('Program executed successfully', 1)[0]
    try:
        values = [int(line.strip()) for line in payload.splitlines() if line.strip()]
    except ValueError:
        print('FAIL: unexpected output', payload)
        return 1
    if len(values) != len(EXPECTED) or any(a != b for a,b in zip(values, EXPECTED)):
        print('FAIL:', values, 'expected:', EXPECTED)
        return 1
    print('PASS: Core integer pacing 17/17')
    return 0

if __name__ == '__main__':
    sys.exit(main())
