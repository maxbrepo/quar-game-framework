"""Validate two independent QGF application sessions in one QRVM process."""
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
    CH / "qgf_sdl3_two_app_sessions_probe.vq",
)
EXPECTED = [
    "1", "true", "true", "2", "1", "video", "0", "2",
    "3", "0", "0", "false", "0", "1", "true", "true",
    "2", "1", "video", "2", "3", "0", "0",
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
    text = "\n".join(
        line for path in PARTS
        for line in path.read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("//")
    )
    with tempfile.TemporaryDirectory(prefix="qgf_ch01_two_sessions_") as tmp:
        file = Path(tmp) / "two_sessions.vq"
        file.write_text(text, encoding="utf-8")
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
    values = result.stdout.split("=== QRVM OUTPUT ===", 1)[1]
    values = values.split("Program executed successfully", 1)[0]
    observed = [line.strip().lower() for line in values.splitlines() if line.strip()]
    if len(observed) != len(EXPECTED):
        print("FAIL: output count", observed)
        return 1
    for actual, expected in zip(observed, EXPECTED):
        if expected == "video":
            if not actual.isdecimal() or int(actual) & 32 != 32:
                print("FAIL: SDL video flags", observed)
                return 1
        elif actual != expected:
            print("FAIL: lifecycle sequence", observed)
            return 1
    print("PASS: 2/2 native SDL3 sessions with separate QGF app lifecycle states")
    return 0


if __name__ == "__main__":
    sys.exit(main())
