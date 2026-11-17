"""Run canonical SDL3 window examples from an external Visual Quar SDK."""
import argparse
import ctypes.util
import subprocess
import sys
from pathlib import Path

TEST_NAME = "test_ch24_73_84_sdl3_vq_windows.py"
EXAMPLES = (
    "24_73_sdl3_window_basic",
    "24_74_sdl3_window_delay",
    "24_75_sdl3_two_windows",
    "24_76_sdl3_reinitialize",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sdk", type=Path, required=True)
    args = parser.parse_args()
    sdk = args.sdk.expanduser().resolve()
    test = sdk / "tests" / TEST_NAME
    examples = sdk / "examples" / "0.0.5" / "typed" / "24_interoperability"
    missing = [str(p) for p in [test, *(examples / (n + ".vq") for n in EXAMPLES)] if not p.is_file()]
    if missing:
        print("BLOCKED: SDK missing required canonical files:")
        for name in missing:
            print(" -", name)
        return 2
    lib = ctypes.util.find_library("SDL3")
    print("SDL3 shared library:", lib or "NOT FOUND")
    print("SDK:", sdk)
    print("Running SDK's canonical tests; QGF does not copy SDK bindings.")
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests",
         "-p", TEST_NAME, "-v"], cwd=sdk, capture_output=True, text=True,
        timeout=120,
    )
    output = result.stdout + result.stderr
    print(output)
    if result.returncode != 0:
        print("FAIL: SDK canonical window tests failed")
        return 1
    if not lib or "skipped 'SDL3 shared library not available'" in output:
        print("PASS: source and metadata checks; BLOCKED: native SDL3 runtime unavailable")
        return 2
    if "test_native_sdl3_window_lifecycle" not in output or "skipped" in output:
        print("UNTESTED: native runtime test not confirmed")
        return 2
    print("PASS: SDK canonical SDL3 window test suite (native runtime included)")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except subprocess.TimeoutExpired:
        print("FAIL: SDK test timed out")
        sys.exit(1)
