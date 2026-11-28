"""Check public platform truthfulness while native SDL3 probe succeeds."""
import ctypes.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SDK = Path(os.environ.get("QUAR_SDK", str(ROOT / "sdk"))).expanduser().resolve()
CH = ROOT / "experimental/marathon2/chapter01"
SOURCES = (
    ROOT / "core/platform.vq",
    ROOT / "core/lifecycle.vq",
    CH / "qgf_lifecycle_transition.vq",
    CH / "qgf_lifecycle_guard.vq",
    CH / "qgf_lifecycle_sequence.vq",
    CH / "qgf_lifecycle_contract.vq",
    CH / "qgf_sdl3_public_platform_boundary_probe.vq",
)
EXPECTED = [
    "true", "true", "false", "false", "true", "3", "3", "0",
    "true", "1", "2", "3", "0", "1", "true", "true", "2", "1",
    "video", "false", "2", "3", "0", "0", "3",
]


def main():
    if not (SDK / "main.py").is_file():
        print("BLOCKED: external Quar SDK missing")
        return 2
    missing = [str(p.relative_to(ROOT)) for p in SOURCES if not p.is_file()]
    if missing:
        print("BLOCKED: missing sources:", ", ".join(missing))
        return 2
    library = ctypes.util.find_library("SDL3")
    if not library:
        print("BLOCKED: SDL3 shared library missing")
        return 2
    combined = "\n".join(
        line for path in SOURCES
        for line in path.read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("//")
    )
    with tempfile.TemporaryDirectory(prefix="qgf_ch01_platform_boundary_") as tmp:
        source = Path(tmp) / "boundary.vq"
        source.write_text(combined, encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, str(SDK / "main.py"),
                 "--native-library", library, "-f", str(source)],
                cwd=SDK, input="1\n", capture_output=True, text=True,
                env={**os.environ, "SDL_VIDEODRIVER": "dummy", "TERM": "dumb"},
                timeout=60,
            )
        except subprocess.TimeoutExpired:
            print("FAIL: QRVM timed out")
            return 1
    if result.returncode or "=== QRVM OUTPUT ===" not in result.stdout or "Program executed successfully" not in result.stdout:
        print("FAIL: QRVM execution")
        print(result.stdout)
        print(result.stderr)
        return 1
    output = result.stdout.split("=== QRVM OUTPUT ===", 1)[1]
    output = output.split("Program executed successfully", 1)[0]
    actual = [line.strip().lower() for line in output.splitlines() if line.strip()]
    if len(actual) != len(EXPECTED):
        print("FAIL: output count", len(actual), "expected", len(EXPECTED), actual)
        return 1
    for index, (value, expected) in enumerate(zip(actual, EXPECTED), 1):
        if expected == "video":
            valid = value.isdecimal() and int(value) & 32 == 32
        else:
            valid = value == expected
        if not valid:
            print("FAIL: public/native boundary at output", index)
            print("Expected:", EXPECTED)
            print("Observed:", actual)
            return 1
    print("PASS: public SDL3 unavailable; NONE backend valid; native SDL3 probe remains operational")
    return 0


if __name__ == "__main__":
    sys.exit(main())
