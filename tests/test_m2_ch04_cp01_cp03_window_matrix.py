"""Regression matrix for existing logical window policies, without SDL3."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SDK = Path(os.environ.get('QUAR_SDK', str(ROOT / 'sdk'))).resolve()

def main():
    lines = [(ROOT / 'core/window.vq').read_text()]
    expected = []
    def check(expr, value):
        lines.append(f'if ({expr} == {str(value).lower()}) {{ print(1); }} else {{ print(0); }}')
        expected.append(1)
    for state in range(4):
        check(f'qgf_window_prepare({state}, 640, 480)', 1 if state == 0 else state)
        check(f'qgf_window_open_state({state})', 2 if state == 1 else state)
        check(f'qgf_window_close({state})', 3 if state in (1, 2) else state)
        check(f'qgf_window_reset({state})', 0 if state == 3 else state)
        for mode in (-1, 0, 1, 2, 3):
            check(f'qgf_window_can_change_mode({state}, {mode})', state == 1 and 0 <= mode <= 2)
        for size in (0, 1, 16384, 16385):
            check(f'qgf_window_resize_valid({state}, {size}, 480)', state == 1 and 1 <= size <= 16384)
        for length in (0, 1, 255, 256):
            check(f'qgf_window_can_change_title({state}, {length})', state != 3 and 1 <= length <= 255)
    for width, height in ((320,240),(800,600),(319,240),(800,601)):
        valid = 320 <= width <= 800 and 240 <= height <= 600
        check(f'qgf_window_dimensions_within_limits({width},{height},320,240,800,600)', valid)
        check(f'qgf_window_choose_width(640,1,{width},{height},320,240,800,600)', width if valid else 640)
        check(f'qgf_window_choose_height(480,1,{width},{height},320,240,800,600)', height if valid else 480)
    for first in range(4):
        for second in range(4):
            for requested in (1,2,3):
                check(f'qgf_window_can_select({requested},1,{first},2,{second})', (requested == 1 and first == 2) or (requested == 2 and second == 2))
    for candidate in (0,1,2,3):
        check(f'qgf_window_id_available({candidate},1,2)', candidate == 3)
    for state in range(4):
        check(f'qgf_window_release_id(1,{state})', 0 if state == 3 else 1)
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / 'window_matrix.vq'
        source.write_text('\n'.join(line for line in '\n'.join(lines).splitlines() if not line.lstrip().startswith('//')))
        result = subprocess.run([sys.executable, str(SDK / 'main.py'), '-f', str(source)], cwd=SDK, input='1\n', text=True, capture_output=True, timeout=90)
    if result.returncode or '=== QRVM OUTPUT ===' not in result.stdout or 'Program executed successfully' not in result.stdout:
        print(result.stdout, result.stderr)
        return 1
    payload = result.stdout.split('=== QRVM OUTPUT ===',1)[1].split('Program executed successfully',1)[0]
    actual = [int(line.strip()) for line in payload.splitlines() if line.strip()]
    if actual != expected:
        print('FAIL:', actual, 'expected:', expected)
        return 1
    print(f'PASS: CP01-CP03 logical window matrix {len(expected)}/{len(expected)}')
    return 0

if __name__ == '__main__':
    sys.exit(main())
