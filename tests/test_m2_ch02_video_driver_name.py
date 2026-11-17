"""SDL3 cstring return probe, separate from the known-good numeric path."""
import argparse
import ctypes.util
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "experimental/marathon2/chapter02/qgf_video_driver_name_probe.vq"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sdk", required=True, type=Path)
    parser.add_argument("--library", type=Path)
    args = parser.parse_args()
    sdk = args.sdk.expanduser().resolve()
    if not (sdk / "main.py").is_file() or not SOURCE.is_file():
        print("BLOCKED: missing SDK or source")
        return 2
    if args.library:
        lib = args.library.expanduser().resolve()
    else:
        name = ctypes.util.find_library("SDL3")
        lib = next((p.resolve() for folder in (
            "/lib/x86_64-linux-gnu", "/usr/lib/x86_64-linux-gnu",
            "/lib/aarch64-linux-gnu", "/usr/lib/aarch64-linux-gnu",
            "/usr/local/lib", "/usr/local/lib64", "/lib", "/usr/lib")
            if name for p in [Path(folder) / name] if p.is_file()), None)
    if not lib or not lib.is_file():
        print("BLOCKED: SDL3 library unavailable")
        return 2
    try:
        result = subprocess.run(
            [sys.executable, str(sdk / "main.py"), "--native-library", str(lib),
             "-f", str(SOURCE)], input="1\n", text=True, capture_output=True,
            cwd=sdk, timeout=45)
    except subprocess.TimeoutExpired:
        print("FAIL: QRVM timeout")
        return 1
    if result.returncode or "Program executed successfully" not in result.stdout:
        print("FAIL: SDL3 cstring probe not completed")
        print(result.stdout)
        print(result.stderr)
        return 1
    output = result.stdout.split("=== QRVM OUTPUT ===", 1)[-1].split(
        "Program executed successfully", 1)[0]
    values = [line.strip() for line in output.splitlines() if line.strip()]
    if not values or values[0].lower() in ("none", "null", "0"):
        print("BLOCKED: no first video driver name available")
        return 2
    print("PASS: SDL3 video driver cstring:", values[0])
    return 0

if __name__ == "__main__":
    sys.exit(main())
