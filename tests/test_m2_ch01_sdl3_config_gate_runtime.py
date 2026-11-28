"""Verify existing QGF configuration gate before native SDL3 startup."""
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
    CH / "qgf_sdl3_config_gate_probe.vq",
)
EXPECTED = [
    "false", "2", "false", "2", "false", "2", "0", "0", "0",
    "true", "1", "true", "2", "1", "video", "2", "3", "0", "0",
]


def main():
    if not (SDK / "main.py").is_file():
        print("BLOCKED: external SDK missing")
        return 2
    missing = [str(path.relative_to(ROOT)) for path in PARTS if not path.is_file()]
    if missing:
        print("BLOCKED: missing QGF sources:", ", ".join(missing))
        return 2
    library = ctypes.util.find_library("SDL3")
    if not library:
        print("BLOCKED: SDL3 shared library missing")
        return 2
    source_text = "\n".join(
        line for path in PARTS
        for line in path.read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("//")
    )
    with tempfile.TemporaryDirectory(prefix="qgf_ch01_config_gate_") as directory:
        source = Path(directory) / "config_gate.vq"
        source.write_text(source_text, encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, str(SDK / "main.py"),
                 "--native-library", library, "-f", str(source)],
                input="1\n", cwd=SDK, capture_output=True, text=True,
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
    output = result.stdout.split("=== QRVM OUTPUT ===", 1)[1]
    output = output.split("Program executed successfully", 1)[0]
    observed = [line.strip().lower() for line in output.splitlines() if line.strip()]
    if len(observed) != len(EXPECTED):
        print("FAIL: unexpected output count", observed)
        return 1
    for actual, expected in zip(observed, EXPECTED):
        if expected == "video":
            if not actual.isdecimal() or (int(actual) & 32) != 32:
                print("FAIL: SDL3 video inactive", observed)
                return 1
        elif actual != expected:
            print("FAIL: configuration or lifecycle mismatch", observed)
            return 1
    print("PASS: QGF configuration gate rejects 3 invalid cases; valid config starts and stops SDL3")
    return 0


if __name__ == "__main__":
    sys.exit(main())
