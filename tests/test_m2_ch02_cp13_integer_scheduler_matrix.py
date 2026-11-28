"""Check integer scheduling against independent arithmetic expectations."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SDK = Path(os.environ.get("QUAR_SDK", str(ROOT / "sdk"))).resolve()

def main():
    core = '\n'.join(line for line in (ROOT / 'core/game_loop.vq').read_text().splitlines() if not line.lstrip().startswith('//'))
    lines = [core]
    expected = []
    for previous in (0, 7, 16, 49):
        for delta in (0, 1, 16, 100):
            for cap in (0, 1, 4):
                total = previous + delta
                steps = min(total // 16, cap)
                lines.extend((f'print(qgf_frame_fixed_steps({previous}, {delta}, 16, {cap}));', f'print(qgf_frame_remaining_ms({previous}, {delta}, 16, {cap}));'))
                expected.extend((steps, total - steps * 16))
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
    print(f'PASS: CP13 integer scheduler matrix {len(expected)}/{len(expected)}')
    return 0

if __name__ == '__main__':
    sys.exit(main())
