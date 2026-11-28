"""Run one vertical app/backend/SDL3 lifecycle in success and failure modes."""
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
    ROOT / "experimental/marathon2/chapter01/qgf_app_backend_native_vertical_probe.vq",
)


def run_case(source, library, driver, expected):
    try:
        result = subprocess.run(
            [sys.executable, str(SDK / "main.py"), "--native-library", library, "-f", str(source)],
            cwd=SDK, input="1\n", text=True, capture_output=True, timeout=60,
            env={**os.environ, "SDL_VIDEODRIVER": driver, "TERM": "dumb"},
        )
    except subprocess.TimeoutExpired:
        print("FAIL: QRVM timeout:", driver)
        return False
    if result.returncode or "=== QRVM OUTPUT ===" not in result.stdout or "Program executed successfully" not in result.stdout:
        print("FAIL: QRVM:", driver, result.stdout, result.stderr)
        return False
    payload = result.stdout.split("=== QRVM OUTPUT ===", 1)[1].split("Program executed successfully", 1)[0]
    observed = [line.strip().lower() for line in payload.splitlines() if line.strip()]
    if len(observed) != len(expected):
        print("FAIL: output count:", driver, observed)
        return False
    for value, wanted in zip(observed, expected):
        if wanted == "video":
            if not value.isdecimal() or int(value) & 32 != 32:
                print("FAIL: video subsystem inactive:", driver, observed)
                return False
        elif value != wanted:
            print("FAIL: unexpected state:", driver, observed, "expected:", expected)
            return False
    return True


def main():
    if not (SDK / "main.py").is_file() or any(not p.is_file() for p in SOURCES):
        print("BLOCKED: SDK or QGF source missing")
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
    with tempfile.TemporaryDirectory(prefix="qgf_cp27_") as tmp:
        source = Path(tmp) / "vertical.vq"
        source.write_text(program, encoding="utf-8")
        success = ["true", "true", "1", "2", "2", "true", "true", "video", "3", "3", "0"]
        failure = ["true", "false", "0", "0", "0", "false", "false", "0", "0", "0", "0"]
        if not run_case(source, library, "dummy", success):
            return 1
        if not run_case(source, library, "__qgf_invalid_video_driver__", failure):
            return 1
    print("PASS: QGF app/backend/SDL3 vertical lifecycle success + native failure (2/2)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
