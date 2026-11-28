"""Verify native SDL3 init failure cannot advance QGF Core backend state."""
import ctypes.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SDK = Path(os.environ.get("QUAR_SDK", str(ROOT / "sdk"))).resolve()
SOURCES = (
    ROOT / "core/platform.vq",
    ROOT / "experimental/marathon2/chapter01/qgf_platform_native_failure_core_probe.vq",
)
EXPECTED = ["false", "false", "0", "false", "false", "false", "0", "false"]


def main():
    if not (SDK / "main.py").is_file():
        print("BLOCKED: external SDK missing")
        return 2
    if any(not path.is_file() for path in SOURCES):
        print("BLOCKED: missing QGF sources")
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
    with tempfile.TemporaryDirectory(prefix="qgf_cp26_") as temp:
        source = Path(temp) / "native_failure.vq"
        source.write_text(program, encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, str(SDK / "main.py"), "--native-library", library, "-f", str(source)],
                cwd=SDK, input="1\n", text=True, capture_output=True, timeout=60,
                env={**os.environ, "SDL_VIDEODRIVER": "__qgf_intentionally_invalid_video_driver__", "TERM": "dumb"},
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
    observed = [line.strip().lower() for line in payload.splitlines() if line.strip()]
    if observed != EXPECTED:
        print("FAIL: native failure was not isolated from Core state")
        print("Expected:", EXPECTED)
        print("Observed:", observed)
        return 1
    print("PASS: native SDL3 failure leaves Core backend CREATED (8/8)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
