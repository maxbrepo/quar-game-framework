"""Logical window lifecycle coordinated with the existing session predicates."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SDK = Path(os.environ.get('QUAR_SDK', str(ROOT / 'sdk'))).resolve()

def main():
    lines = [(ROOT / 'core' / name).read_text() for name in ('lifecycle.vq', 'platform.vq', 'session.vq', 'window.vq')]
    expected = []
    def check(expr, value):
        lines.append(f'if (({expr}) == {str(value).lower()}) {{ print(1); }} else {{ print(0); }}')
        expected.append(1)
    for app in (-1,0,1,2,3,4):
        for backend in (-1,0,1,2,3,4):
            for window in (-1,0,1,2,3,4):
                check(f'qgf_session_running({app},{backend}) and qgf_window_can_open({window})', app == 2 and backend == 2 and window == 1)
    lines.extend(['int window_state = qgf_window_prepare(qgf_window_created(),640,480);', 'window_state = qgf_window_open_state(window_state);'])
    check('window_state',2)
    lines.append('window_state = qgf_window_close(window_state);')
    check('window_state',3)
    lines.append('window_state = qgf_window_reset(window_state);')
    check('window_state',0)
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / 'window_session.vq'
        source.write_text('\n'.join(line for line in '\n'.join(lines).splitlines() if not line.lstrip().startswith('//')))
        result = subprocess.run([sys.executable,str(SDK / 'main.py'),'-f',str(source)],cwd=SDK,input='1\n',text=True,capture_output=True,timeout=90)
    if result.returncode or '=== QRVM OUTPUT ===' not in result.stdout or 'Program executed successfully' not in result.stdout:
        print(result.stdout,result.stderr)
        return 1
    payload = result.stdout.split('=== QRVM OUTPUT ===',1)[1].split('Program executed successfully',1)[0]
    actual = [int(line.strip()) for line in payload.splitlines() if line.strip()]
    if actual != expected:
        print('FAIL:',actual)
        return 1
    print(f'PASS: CP05 window session coordination {len(expected)}/{len(expected)}')
    return 0

if __name__ == '__main__':
    sys.exit(main())
