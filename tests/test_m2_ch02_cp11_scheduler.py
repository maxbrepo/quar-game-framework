"""Execute the actual demo's fixed-update block without native SDL dependencies."""
from pathlib import Path
import subprocess
import sys
import tempfile
import os
ROOT = Path(__file__).resolve().parents[1]
SDK = Path(os.environ.get('QUAR_SDK', str(ROOT / 'sdk'))).resolve()
DEMO = ROOT / 'demos/0.0.2/02_game_loop/009_pause_render_independence/main.vq'

def main():
    source = DEMO.read_text()
    start = source.index('    if (state == running_state) {\n        int steps_due')
    end = source.index('    if (state != stopping_state) {\n        SDL_SetRenderDrawColorFloat', start)
    block = source[start:end]
    prefix = '''int running_state = 0;
int state = 0;
int fixed_step_ms = 16;
int simulation_delta_ms = 16;
int accumulator_ms = 0;
int max_steps = 4;
f32 position_x = 90.0;
f32 step_x = 2.0;
u64 update_count = 0;
u64 one_frame = 1;
int frame = 0;
while (frame < 60) {
    if (frame == 15) { state = 1; }
    if (frame == 30) { state = 0; }
'''
    suffix = '''    frame = frame + 1;
}
print(update_count);
print(accumulator_ms);
print(position_x);
simulation_delta_ms = 100;
''' + block + '''print(update_count);
print(accumulator_ms);
state = 1;
''' + block + '''print(update_count);
print(accumulator_ms);
'''
    core = '\n'.join(line for line in (ROOT / 'core/game_loop.vq').read_text().splitlines() if not line.lstrip().startswith('//'))
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / 'scheduler.vq'
        p.write_text(core + '\n' + prefix + block + suffix)
        r = subprocess.run([sys.executable, str(SDK / 'main.py'), '-f', str(p)], cwd=SDK, input='1\n', text=True, capture_output=True, timeout=90)
    if r.returncode or '=== QRVM OUTPUT ===' not in r.stdout or 'Program executed successfully' not in r.stdout:
        print(r.stdout, r.stderr)
        return 1
    payload = r.stdout.split('=== QRVM OUTPUT ===', 1)[1].split('Program executed successfully', 1)[0]
    values = [float(line.strip()) for line in payload.splitlines() if line.strip()]
    if values != [45, 0, 180, 49, 36, 49, 36]:
        print('FAIL:', values)
        return 1
    print('PASS: CP11 shared fixed scheduler 7/7')
    return 0

if __name__ == '__main__':
    sys.exit(main())
