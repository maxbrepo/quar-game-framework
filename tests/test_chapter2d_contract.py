from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "demos/0.0.2/02_game_loop"

def test_demos():
    for name in ("002_fixed_timestep_line", "003_frame_pacing_line"):
        directory = BASE / name
        source = (directory / "main.vq").read_text()
        meta = json.loads((directory / "demo.json").read_text())
        assert meta["chapter"] == 2
        assert "QGF_DEMO_OK" in source
        assert "bool batch_mode = false;" in source

def test_timing_strategies():
    assert "while (accumulator_ms >= step_ms)" in (BASE / "002_fixed_timestep_line/main.vq").read_text()
    assert "SDL_Delay(1)" in (BASE / "003_frame_pacing_line/main.vq").read_text()
