"""Run QGF SDL3 probes against the external, unmodified Visual Quar SDK."""
import argparse
import ctypes.util
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CASES = (
    ("chapter01/qgf_sdl3_init_bool_probe.vq", "dummy"),
    ("chapter02/qgf_video_driver_name_probe.vq", "dummy"),
    ("chapter02/qgf_sdl3_visible_window.vq", "visible"),
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sdk", type=Path, default=Path("sdk"))
    parser.add_argument("--visible", action="store_true", help="Display an actual SDL3 window")
    args = parser.parse_args()
    sdk = args.sdk.resolve()
    library = ctypes.util.find_library("SDL3")
    if not (sdk / "main.py").is_file():
        print("BLOCKED: external SDK main.py missing")
        return 2
    if not library:
        print("BLOCKED: SDL3 shared library unavailable")
        return 2
    statuses = []
    for rel, mode in CASES:
        if mode == "visible" and not args.visible:
            print("UNTESTED:", rel, "(enable --visible)")
            continue
        path = ROOT / "experimental" / "marathon2" / rel
        if not path.is_file():
            print("BLOCKED: missing", path)
            statuses.append(2)
            continue
        env = os.environ.copy()
        if mode == "dummy":
            env["SDL_VIDEODRIVER"] = "dummy"
        else:
            env.pop("SDL_VIDEODRIVER", None)
        command = [sys.executable, str(Path(__file__).resolve()), "--_case", str(sdk), str(path), library]
        try:
            result = subprocess.run(command, capture_output=True, text=True, env=env, timeout=15)
        except subprocess.TimeoutExpired:
            print("FAIL: timeout", rel)
            statuses.append(1)
            continue
        print(("PASS" if result.returncode == 0 else "FAIL") + ":", rel)
        if result.stdout.strip():
            print(result.stdout.strip())
        if result.stderr.strip():
            print(result.stderr.strip())
        statuses.append(0 if result.returncode == 0 else 1)
    return max(statuses, default=2)


def run_case(sdk, source, library):
    sys.path.insert(0, str(sdk))
    from frontend.quar.lexer import Lexer
    from frontend.quar.parser import Parser
    from frontend.quar.semantic import SemanticAnalyzer
    from main import run_qrvm
    program = Parser(Lexer(source.read_text(encoding="utf-8")).tokenize()).parse()
    SemanticAnalyzer().analyze(program)
    # Only the window example declares an opaque native release function.
    release_symbols = ("SDL_DestroyWindow",) if source.name == "qgf_sdl3_visible_window.vq" else ()
    run_qrvm(program, native_library=library, native_release_symbols=release_symbols)
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 5 and sys.argv[1] == "--_case":
        sys.exit(run_case(Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]))
    sys.exit(main())
