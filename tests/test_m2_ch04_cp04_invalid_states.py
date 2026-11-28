"""Invalid-state regression for logical window policies, without SDL3."""
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
    for state in (-2, -1, 4, 5, 99):
        check(f'qgf_window_prepare({state},640,480)', state)
        check(f'qgf_window_open_state({state})', state)
        check(f'qgf_window_close({state})', state)
        check(f'qgf_window_reset({state})', state)
        check(f'qgf_window_can_change_title({state},10)', False)
        check(f'qgf_window_can_change_mode({state},1)', False)
        check(f'qgf_window_resize_valid({state},640,480)', False)
        check(f'qgf_window_can_remove(1,{state})', False)
        check(f'qgf_window_can_select(1,1,{state},2,2)', False)
    for state in range(4):
        check(f'qgf_window_can_change_title({state},10)', state != 3)
        check(f'qgf_window_change_mode(0,{state},99)', 0)
    for first, second in ((0,2),(1,1),(-1,2)):
        check(f'qgf_window_can_select(2,{first},2,{second},2)', False)
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
    print(f'PASS: CP04 invalid window states {len(expected)}/{len(expected)}')
    return 0

if __name__ == '__main__':
    sys.exit(main())
