"""Check guard decisions and two real SDL3 lifecycle cycles in one QRVM run."""
import ctypes.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SDK = Path(os.environ.get("QUAR_SDK", str(ROOT / "sdk"))).expanduser().resolve()
DIRECTORY = ROOT / "experimental/marathon2/chapter01"
PARTS = (
    "qgf_lifecycle_transition.vq", "qgf_lifecycle_guard.vq",
    "qgf_lifecycle_sequence.vq", "qgf_lifecycle_contract.vq",
    "qgf_sdl3_guarded_cycles_probe.vq",
)


def main():
    if not (SDK / "main.py").is_file():
        print("BLOCKED: external Quar SDK missing")
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
    try:
        with tempfile.TemporaryDirectory(prefix="qgf_guarded_cycles_") as temp:
            program = Path(temp) / "guarded_cycles.vq"
            program.write_text(source_text, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SDK / "main.py"), "--native-library", library,
                 "-f", str(program)],
                cwd=SDK, input="1\n", capture_output=True, text=True,
                env={**os.environ, "SDL_VIDEODRIVER": "dummy", "TERM": "dumb"},
                timeout=45,
            )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print("FAIL:", exc)
        return 1
    if (result.returncode or "=== QRVM OUTPUT ===" not in result.stdout
            or "Program executed successfully" not in result.stdout):
        print("FAIL: QRVM execution")
        print(result.stdout)
        print(result.stderr)
        return 1
    output = result.stdout.split("=== QRVM OUTPUT ===", 1)[1].split("Program executed successfully", 1)[0]
    observed = [line.strip().lower() for line in output.splitlines() if line.strip()]
    expected = [
        "1", "1", "true", "0", "false", "video", "2", "0", "true", "0",
        "0", "false", "1", "1", "true", "video", "2", "0", "true", "0",
    ]
    if len(observed) != len(expected):
        print("FAIL: output count", len(observed), "expected", len(expected), observed)
        return 1
    for index, (actual, wanted) in enumerate(zip(observed, expected)):
        if wanted == "video":
            valid = actual.isdecimal() and (int(actual) & 32) == 32
        else:
            valid = actual == wanted
        if not valid:
            print("FAIL: mismatch at", index, "expected", wanted, "observed", actual)
            return 1
    print("PASS: guarded SDL3 lifecycle, duplicate actions denied, 2/2 native cycles")
    return 0


if __name__ == "__main__":
    sys.exit(main())
