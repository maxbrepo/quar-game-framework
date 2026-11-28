import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / 'demos/0.0.2/02_game_loop/009_pause_render_independence'


def test_metadata_and_independent_counters():
    metadata = json.loads((DEMO / 'demo.json').read_text())
    source = (DEMO / 'main.vq').read_text()
    assert metadata['batch_frames'] == 60
    assert 'u64 expected_updates = 45;' in source
    assert 'u64 expected_renders = 60;' in source
    assert 'update_count = update_count + one_frame;' in source
    assert 'render_count = render_count + one_frame;' in source
    assert source.index('if (frame_count == pause_at)') < source.index('if (qgf_loop_can_update(state)) {\n        int steps_due')
    assert source.count('SDL_RenderPresent(renderer);') == 1
    assert 'QGF_DEMO_OK' in source


def test_simulated_state_transitions():
    state = 'running'
    updates = 0
    renders = 0
    for frame in range(60):
        if frame == 15:
            state = 'paused'
        if frame == 30:
            state = 'running'
        if state == 'running':
            updates += 1
        renders += 1
    assert (updates, renders) == (45, 60)


def test_stopping_state_cannot_be_overridden_by_timed_transitions():
    source = (DEMO / 'main.vq').read_text()
    assert 'if (qgf_loop_can_render(state)) {\n        if (frame_count == pause_at)' in source
    assert 'if (frame_count == resume_at) { state = qgf_loop_resume(state); }' in source
    assert source.rindex('SDL_DestroyRenderer(renderer);') < source.rindex('SDL_DestroyWindow(window);') < source.index('qgf_sdl3_close();', source.index('SDL_DestroyWindow(window);'))


def test_stop_event_skips_render_and_frame_increment():
    source = (DEMO / 'main.vq').read_text()
    guard = source.index('    if (qgf_loop_can_render(state)) {\n        SDL_SetRenderDrawColorFloat')
    present = source.index('        SDL_RenderPresent(renderer);', guard)
    count = source.index('        frame_count = frame_count + one_frame;', present)
    end_guard = source.index('    }\n    if (batch_mode)', count)
    assert guard < present < count < end_guard
    assert 'SDL_RenderPresent(renderer);' not in source[end_guard:]


def test_stop_during_running_or_pause_is_terminal():
    """Model the source's event priority for early termination."""
    for stop_frame in (8, 20, 30, 59):
        state = 'running'
        updates = 0
        renders = 0
        for frame in range(60):
            if frame == stop_frame:
                state = 'stopping'
            if state != 'stopping':
                if frame == 15:
                    state = 'paused'
                if frame == 30:
                    state = 'running'
            if state == 'running':
                updates += 1
            if state != 'stopping':
                renders += 1
            if state == 'stopping':
                break
        assert renders == stop_frame
        assert updates == stop_frame - max(0, min(stop_frame, 30) - 15)
        assert state == 'stopping'


def test_source_event_priority_and_cleanup_after_loop():
    source = (DEMO / 'main.vq').read_text()
    loop = source.index('while (running) {')
    pump = source.index('SDL_PumpEvents();', loop)
    quit_event = source.index('if (SDL_HasEvent(quit_event))', pump)
    key_event = source.index('if (SDL_HasEvent(key_event))', quit_event)
    transitions = source.index('if (qgf_loop_can_render(state)) {', key_event)
    updates = source.index('if (qgf_loop_can_update(state)) {\n        int steps_due', transitions)
    render_guard = source.index('if (qgf_loop_can_render(state)) {\n        SDL_SetRenderDrawColorFloat', updates)
    exit_guard = source.index('if (state == stopping_state) { running = false; }', render_guard)
    cleanup = source.index('SDL_DestroyRenderer(renderer);', exit_guard)
    assert loop < pump < quit_event < key_event < transitions < updates < render_guard < exit_guard < cleanup
