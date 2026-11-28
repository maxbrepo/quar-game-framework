"""Validate reusable QGF session guards against real SDL3 success and failure."""
import ctypes.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SDK = Path(os.environ.get("QUAR_SDK", str(ROOT / "sdk"))).resolve()
SOURCES = (
    ROOT / "core/lifecycle.vq",
    ROOT / "core/platform.vq",
    ROOT / "core/session.vq",
    ROOT / "experimental/marathon2/chapter01/qgf_session_native_probe.vq",
)


def run_case(source, library, driver, expected):
    try:
        result = subprocess.run(
            [sys.executable, str(SDK / "main.py"), "--native-library", library, "-f", str(source)],
            cwd=SDK, input="1\n", capture_output=True, text=True, timeout=60,
            env={**os.environ, "SDL_VIDEODRIVER": driver, "TERM": "dumb"},
        )
    except subprocess.TimeoutExpired:
        print("FAIL: QRVM timeout:", driver)
        return False
    if result.returncode or "=== QRVM OUTPUT ===" not in result.stdout or "Program executed successfully" not in result.stdout:
        print("FAIL: QRVM execution:", driver, result.stdout, result.stderr)
        return False
    payload = result.stdout.split("=== QRVM OUTPUT ===", 1)[1].split("Program executed successfully", 1)[0]
    values = [line.strip().lower() for line in payload.splitlines() if line.strip()]
    if values != expected:
        print("FAIL: session coordination:", driver)
        print("Expected:", expected)
        print("Observed:", values)
        return False
    return True


def main():
    if not (SDK / "main.py").is_file() or any(not p.is_file() for p in SOURCES):
        print("BLOCKED: missing SDK or QGF sources")
        return 2
    library = ctypes.util.find_library("SDL3")
    if not library:
        print("BLOCKED: SDL3 missing")
        return 2
    program = "\n".join(
        line for path in SOURCES
        for line in path.read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("//")
    )
    with tempfile.TemporaryDirectory(prefix="qgf_cp28_") as tmp:
        source = Path(tmp) / "session.vq"
        source.write_text(program, encoding="utf-8")
        success = ["false", "true", "true", "1", "true", "true", "true", "true", "3", "3", "0"]
        failure = ["false", "false", "false", "0", "false", "false", "false", "false", "0", "0", "0"]
        if not run_case(source, library, "dummy", success):
            return 1
        if not run_case(source, library, "__qgf_invalid_video_driver__", failure):
            return 1
    print("PASS: QGF session coordination native success + failure (2/2)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
