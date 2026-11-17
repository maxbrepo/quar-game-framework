from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "demos/0.0.2/02_game_loop/008_game_loop_states"

def test_state_demo_contract():
    source = (DEMO / "main.vq").read_text(encoding="utf-8")
    metadata = json.loads((DEMO / "demo.json").read_text(encoding="utf-8"))
    assert metadata["batch_frames"] == 60
    assert "bool batch_mode = false;" in source
    assert "if (frame_count >= max_frames)" in source
    assert "state = paused_state;" in source
    assert "state = running_state;" in source
    assert "state = terminated_state;" in source
    assert source.count("SDL_RenderPresent(renderer);") == 1
    assert "QGF_DEMO_OK" in source


def test_state_demo_lexes_with_bundled_sdk():
    from sdk.frontend.quar.lexer import Lexer
    source = (DEMO / "main.vq").read_text(encoding="utf-8")
    assert Lexer(source).tokenize()
