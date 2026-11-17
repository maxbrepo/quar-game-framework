from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def test_demo_metadata():
    path = ROOT / "demos/0.0.2/02_game_loop/001_delta_time_moving_line"
    meta = json.loads((path / "demo.json").read_text())
    assert meta["chapter"] == 2 and meta["batch_frames"] == 60
    assert "QGF_DEMO_OK" in (path / "main.vq").read_text()

def test_time_module_available():
    assert "qgf_time_clamped_delta_ms" in (ROOT / "core/time.vq").read_text()
