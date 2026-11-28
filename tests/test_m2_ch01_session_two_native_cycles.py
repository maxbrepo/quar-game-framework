"""Two consecutive native SDL3 sessions using canonical QGF Core coordination."""
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
    ROOT / "experimental/marathon2/chapter01/qgf_session_two_native_cycles_probe.vq",
)
EXPECTED = [
    "true", "true", "video", "true", "0", "0", "0",
    "true", "true", "video", "true", "0", "2", "false",
]


def main():
    if not (SDK / "main.py").is_file() or any(not path.is_file() for path in SOURCES):
        print("BLOCKED: SDK or Core source missing")
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
    with tempfile.TemporaryDirectory(prefix="qgf_cp30_") as tmp:
        source = Path(tmp) / "two_sessions.vq"
        source.write_text(program, encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, str(SDK / "main.py"), "--native-library", library, "-f", str(source)],
                cwd=SDK, input="1\n", capture_output=True, text=True, timeout=75,
                env={**os.environ, "SDL_VIDEODRIVER": "dummy", "TERM": "dumb"},
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
    if len(values) != len(EXPECTED):
        print("FAIL: unexpected output count", values)
        return 1
    for observed, expected in zip(values, EXPECTED):
        if expected == "video":
            if not observed.isdecimal() or (int(observed) & 32) != 32:
                print("FAIL: SDL3 video subsystem inactive", values)
                return 1
        elif observed != expected:
            print("FAIL: unexpected lifecycle result", values)
            return 1
    print("PASS: QGF Core two consecutive native SDL3 sessions (14/14)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
