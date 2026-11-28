"""Run existing QGF lifecycle policy with native SDL3 in one QRVM program."""
import ctypes.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SDK = Path(os.environ.get("QUAR_SDK", str(ROOT / "sdk"))).expanduser().resolve()
PARTS = [
    "qgf_lifecycle_transition.vq",
    "qgf_lifecycle_guard.vq",
    "qgf_lifecycle_sequence.vq",
    "qgf_lifecycle_contract.vq",
    "qgf_sdl3_contract_integration_probe.vq",
]
DIRECTORY = ROOT / "experimental/marathon2/chapter01"


def main():
    if not (SDK / "main.py").is_file():
        print("BLOCKED: external SDK missing")
        return 2
    library = ctypes.util.find_library("SDL3")
    if not library:
        print("BLOCKED: SDL3 shared library missing")
        return 2
    source_text = "\n".join(
        line for name in PARTS
        for line in (DIRECTORY / name).read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("//")
    )
    with tempfile.TemporaryDirectory(prefix="qgf_ch01_contract_") as directory:
        source = Path(directory) / "contract_integration.vq"
        source.write_text(source_text, encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, str(SDK / "main.py"), "--native-library", library,
                 "-f", str(source)],
                input="1\n", capture_output=True, text=True, cwd=SDK,
                env={**os.environ, "SDL_VIDEODRIVER": "dummy", "TERM": "dumb"},
                timeout=45,
            )
        except subprocess.TimeoutExpired:
            print("FAIL: QRVM execution timed out")
            return 1
    if result.returncode or "=== QRVM OUTPUT ===" not in result.stdout or "Program executed successfully" not in result.stdout:
        print("FAIL: QRVM execution")
        print(result.stdout)
        print(result.stderr)
        return 1
    payload = result.stdout.split("=== QRVM OUTPUT ===", 1)[1].split("Program executed successfully", 1)[0]
    values = [line.strip().lower() for line in payload.splitlines() if line.strip()]
    expected = ["1", "true", "1", "32", "2", "true", "0", "0"]
    if len(values) != len(expected) or values[0:3] != expected[0:3] or values[4:] != expected[4:] or not values[3].isdecimal() or int(values[3]) & 32 != 32:
        print("FAIL: lifecycle/SDL3 contract mismatch")
        print("Actual:", values)
        return 1
    print("PASS: existing QGF lifecycle contract -> SDL_Init -> SDL_Quit -> STOPPED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
