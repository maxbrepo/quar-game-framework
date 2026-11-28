"""Run the published headless example with an intentionally invalid SDL3 video driver.

The same application must reject native initialization without advancing its session.
"""
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
    ROOT / "core/sdl3_session.vq",
    ROOT / "examples/0.0.2/typed/01 core/qgf_headless_sdl3_session.vq",
)


def main():
    if not (SDK / "main.py").is_file() or any(not p.is_file() for p in SOURCES):
        print("BLOCKED: SDK or QGF sources missing")
        return 2
    library = ctypes.util.find_library("SDL3")
    if not library:
        print("BLOCKED: SDL3 library missing")
        return 2
    program = "\n".join(
        line for path in SOURCES
        for line in path.read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("//")
    )
    with tempfile.TemporaryDirectory(prefix="qgf_cp33_") as temp:
        source = Path(temp) / "headless_native_failure.vq"
        source.write_text(program, encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, str(SDK / "main.py"), "--native-library", library, "-f", str(source)],
                cwd=SDK, input="1\n", capture_output=True, text=True, timeout=75,
                env={**os.environ, "SDL_VIDEODRIVER": "__qgf_invalid_driver_cp33__", "TERM": "dumb"},
            )
        except subprocess.TimeoutExpired:
            print("FAIL: QRVM timeout")
            return 1
    if result.returncode or "=== QRVM OUTPUT ===" not in result.stdout or "Program executed successfully" not in result.stdout:
        print("FAIL: QRVM execution")
        print(result.stdout)
        print(result.stderr)
        return 1
    payload = result.stdout.split("=== QRVM OUTPUT ===", 1)[1].split("Program executed successfully", 1)[0]
    values = [line.strip().lower() for line in payload.splitlines() if line.strip()]
    if values != ["0"]:
        print("FAIL: headless example should reject native failure", values)
        return 1
    print("PASS: reusable QGF headless example rejects SDL3 native failure (1/1)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
