"""Native SDL3 failure and success paths, using existing QGF lifecycle functions."""
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
    "qgf_lifecycle_transition.vq",
    "qgf_lifecycle_guard.vq",
    "qgf_lifecycle_sequence.vq",
    "qgf_lifecycle_contract.vq",
    "qgf_sdl3_native_failure_probe.vq",
)


def run_probe(source, library, driver):
    env = os.environ.copy()
    env["SDL_VIDEODRIVER"] = driver
    env["TERM"] = "dumb"
    result = subprocess.run(
        [sys.executable, str(SDK / "main.py"), "--native-library", library,
         "-f", str(source)],
        input="1\n", capture_output=True, text=True, cwd=SDK,
        env=env, timeout=45,
    )
    if (result.returncode != 0 or "=== QRVM OUTPUT ===" not in result.stdout
            or "Program executed successfully" not in result.stdout):
        raise RuntimeError(
            "QRVM failed with SDL_VIDEODRIVER=" + driver
            + "\n" + result.stdout + "\n" + result.stderr
        )
    output = result.stdout.split("=== QRVM OUTPUT ===", 1)[1]
    output = output.split("Program executed successfully", 1)[0]
    return [line.strip().lower() for line in output.splitlines() if line.strip()]


def check(values, expected):
    if len(values) != len(expected):
        return False
    for actual, wanted in zip(values, expected):
        if wanted == "video":
            if not actual.isdecimal() or (int(actual) & 32) != 32:
                return False
        elif actual != wanted:
            return False
    return True


def main():
    if not (SDK / "main.py").is_file():
        print("BLOCKED: Quar SDK missing")
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
        with tempfile.TemporaryDirectory(prefix="qgf_ch01_native_failure_") as tmp:
            source = Path(tmp) / "native_failure.vq"
            source.write_text(source_text, encoding="utf-8")
            failed = run_probe(source, library, "qgf_nonexistent_video_driver")
            succeeded = run_probe(source, library, "dummy")
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print("FAIL:", exc)
        return 1
    if not check(failed, ["1", "false", "2", "true", "0", "0", "3", "0"]):
        print("FAIL: native SDL3 initialization failure did not follow ERROR -> RESET")
        print("Observed:", failed)
        return 1
    if not check(succeeded, ["1", "true", "1", "true", "video", "2", "0", "0"]):
        print("FAIL: normal SDL3 initialization/shutdown mismatch")
        print("Observed:", succeeded)
        return 1
    print("PASS: real SDL3 failure -> ERROR -> RESET; separate SDL3 success -> ACTIVE -> STOPPED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
