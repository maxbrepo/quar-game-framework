"""Check scheduler and loop state coordination."""
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
    # Exercise the same update/render gates used by demo 009.
    lines.append("int state = qgf_loop_running(); int remaining = 7; int updates = 0; int renders = 0;")
    for action, delta, count, remainder, rendered, state in [
        ('', 12, 1, 3, 1, 0),
        ('pause', 100, 1, 3, 2, 1),
        ('', 200, 1, 3, 3, 1),
        ('resume', 13, 2, 0, 4, 0),
        ('', 100, 6, 36, 5, 0),
        ('stop', 16, 6, 36, 5, 2),
        ('finish', 16, 6, 36, 5, 3),
    ]:
        if action:
            lines.append(f"state = qgf_loop_{action}(state);")
        lines.append(f"if (qgf_loop_can_update(state)) {{ updates = updates + qgf_frame_fixed_steps(remaining, {delta}, 16, 4); remaining = qgf_frame_remaining_ms(remaining, {delta}, 16, 4); }}")
        lines.append("if (qgf_loop_can_render(state)) { renders = renders + 1; }")
        lines.append("print(updates); print(remaining); print(renders); print(state);")
        expected.extend([count, remainder, rendered, state])
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
    print(f'PASS: CP15 scheduler state coordination {len(expected)}/{len(expected)}')
    return 0

if __name__ == '__main__':
    sys.exit(main())
