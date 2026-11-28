"""Verify Core backend transition gated by actual SDL3 initialization."""
import ctypes.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SDK = Path(os.environ.get("QUAR_SDK", str(ROOT / "sdk"))).resolve()
PARTS = (ROOT / "core/platform.vq", ROOT / "experimental/marathon2/chapter01/qgf_platform_verified_native_probe.vq")
EXPECTED = ["1", "0", "false", "false", "true", "1", "true", "2", "video", "false", "3", "0", "0", "false"]


def main():
    if not (SDK / "main.py").is_file():
        print("BLOCKED: external SDK missing")
        return 2
    if any(not path.is_file() for path in PARTS):
        print("BLOCKED: QGF source missing")
        return 2
    lib = ctypes.util.find_library("SDL3")
    if not lib:
        print("BLOCKED: SDL3 library missing")
        return 2
    text = "\n".join(
        line for path in PARTS for line in path.read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("//")
    )
    with tempfile.TemporaryDirectory(prefix="qgf_cp24_") as tmp:
        path = Path(tmp) / "probe.vq"
        path.write_text(text, encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, str(SDK / "main.py"), "--native-library", lib, "-f", str(path)],
                cwd=SDK, input="1\n", text=True, capture_output=True,
                env={**os.environ, "SDL_VIDEODRIVER": "dummy", "TERM": "dumb"},
                timeout=60,
            )
        except subprocess.TimeoutExpired:
            print("FAIL: QRVM timeout")
            return 1
    if result.returncode or "=== QRVM OUTPUT ===" not in result.stdout or "Program executed successfully" not in result.stdout:
        print("FAIL: QRVM execution", result.stdout, result.stderr)
        return 1
    payload = result.stdout.split("=== QRVM OUTPUT ===", 1)[1].split("Program executed successfully", 1)[0]
    values = [line.strip().lower() for line in payload.splitlines() if line.strip()]
    if len(values) != len(EXPECTED):
        print("FAIL: unexpected output count", values)
        return 1
    for actual, expected in zip(values, EXPECTED):
        if expected == "video":
            if not actual.isdecimal() or int(actual) & 32 != 32:
                print("FAIL: video inactive", values)
                return 1
        elif actual != expected:
            print("FAIL: transition mismatch", values)
            return 1
    print("PASS: Core verified SDL3 prepare -> READY -> ACTIVE -> STOPPED -> CREATED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
