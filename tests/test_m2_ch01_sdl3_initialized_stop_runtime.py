"""Test stopping an initialized (not running) QGF app with native SDL3."""
import ctypes.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SDK = Path(os.environ.get("QUAR_SDK", str(ROOT / "sdk"))).expanduser().resolve()
CH = ROOT / "experimental/marathon2/chapter01"
PARTS = (
    ROOT / "core/lifecycle.vq",
    CH / "qgf_lifecycle_transition.vq",
    CH / "qgf_lifecycle_guard.vq",
    CH / "qgf_lifecycle_sequence.vq",
    CH / "qgf_lifecycle_contract.vq",
    CH / "qgf_sdl3_initialized_stop_probe.vq",
)
EXPECTED = [
    "false", "0", "1", "true", "1", "1", "true", "true",
    "video", "2", "3", "0", "0", "false", "false", "false",
    "0", "1",
]


def main():
    if not (SDK / "main.py").is_file():
        print("BLOCKED: Quar SDK missing")
        return 2
    missing = [str(p.relative_to(ROOT)) for p in PARTS if not p.is_file()]
    if missing:
        print("BLOCKED: missing sources:", ", ".join(missing))
        return 2
    library = ctypes.util.find_library("SDL3")
    if not library:
        print("BLOCKED: SDL3 library missing")
        return 2
    combined = "\n".join(
        line for path in PARTS
        for line in path.read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("//")
    )
    with tempfile.TemporaryDirectory(prefix="qgf_ch01_init_stop_") as tmp:
        file = Path(tmp) / "initialized_stop.vq"
        file.write_text(combined, encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, str(SDK / "main.py"),
                 "--native-library", library, "-f", str(file)],
                cwd=SDK, input="1\n", capture_output=True, text=True,
                env={**os.environ, "SDL_VIDEODRIVER": "dummy", "TERM": "dumb"},
                timeout=45,
            )
        except subprocess.TimeoutExpired:
            print("FAIL: QRVM timeout")
            return 1
    if result.returncode or "=== QRVM OUTPUT ===" not in result.stdout or "Program executed successfully" not in result.stdout:
        print("FAIL: QRVM execution")
        print(result.stdout)
        print(result.stderr)
        return 1
    payload = result.stdout.split("=== QRVM OUTPUT ===", 1)[1]
    payload = payload.split("Program executed successfully", 1)[0]
    values = [line.strip().lower() for line in payload.splitlines() if line.strip()]
    if len(values) != len(EXPECTED):
        print("FAIL: output count", values)
        return 1
    for actual, expected in zip(values, EXPECTED):
        if expected == "video":
            if not actual.isdecimal() or int(actual) & 32 != 32:
                print("FAIL: SDL3 video inactive", values)
                return 1
        elif actual != expected:
            print("FAIL: state mismatch", values)
            return 1
    print("PASS: native SDL3 INITIALIZED -> STOPPED without RUNNING; invalid app transitions denied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
