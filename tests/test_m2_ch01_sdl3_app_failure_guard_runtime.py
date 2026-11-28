"""Check application state on real SDL3 initialization failure and success."""
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
    CH / "qgf_sdl3_app_failure_guard_probe.vq",
)


def run(source, library, driver):
    result = subprocess.run(
        [sys.executable, str(SDK / "main.py"), "--native-library", library,
         "-f", str(source)],
        input="1\n", text=True, capture_output=True, cwd=SDK,
        env={**os.environ, "SDL_VIDEODRIVER": driver, "TERM": "dumb"},
        timeout=45,
    )
    if (result.returncode or "=== QRVM OUTPUT ===" not in result.stdout
            or "Program executed successfully" not in result.stdout):
        raise RuntimeError(result.stdout + "\n" + result.stderr)
    body = result.stdout.split("=== QRVM OUTPUT ===", 1)[1]
    body = body.split("Program executed successfully", 1)[0]
    return [line.strip().lower() for line in body.splitlines() if line.strip()]


def check(actual, expected):
    if len(actual) != len(expected):
        return False
    for value, target in zip(actual, expected):
        if target == "video":
            if not value.isdecimal() or int(value) & 32 != 32:
                return False
        elif value != target:
            return False
    return True


def main():
    if not (SDK / "main.py").is_file():
        print("BLOCKED: external Quar SDK missing")
        return 2
    missing = [str(p.relative_to(ROOT)) for p in PARTS if not p.is_file()]
    if missing:
        print("BLOCKED: missing sources:", ", ".join(missing))
        return 2
    library = ctypes.util.find_library("SDL3")
    if not library:
        print("BLOCKED: SDL3 shared library missing")
        return 2
    combined = "\n".join(
        line for path in PARTS
        for line in path.read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("//")
    )
    try:
        with tempfile.TemporaryDirectory(prefix="qgf_ch01_app_failure_") as temp:
            source = Path(temp) / "app_failure.vq"
            source.write_text(combined, encoding="utf-8")
            failure = run(source, library, "qgf_nonexistent_video_driver")
            success = run(source, library, "dummy")
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print("FAIL:", exc)
        return 1
    failed_expected = ["1", "false", "2", "true", "0", "false", "0", "0", "0", "3", "0", "0"]
    passed_expected = ["1", "true", "1", "true", "1", "true", "2", "video", "2", "3", "0", "0"]
    if not check(failure, failed_expected):
        print("FAIL: application advanced after native SDL3 error", failure)
        return 1
    if not check(success, passed_expected):
        print("FAIL: application did not follow native SDL3 success", success)
        return 1
    print("PASS: native SDL3 failure keeps app CREATED; success advances app RUNNING then STOPPED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
