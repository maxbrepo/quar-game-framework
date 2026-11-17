"""Run chapter 2 probes; optionally repeat chapter 1 native regression batch."""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sdk", required=True, type=Path)
    parser.add_argument("--library", type=Path)
    parser.add_argument("--include-ch01", action="store_true")
    args = parser.parse_args()
    sdk = args.sdk.expanduser().resolve()
    tasks = [
        ("SDL3 driver count i32", "test_m2_ch02_video_drivers.py"),
        ("SDL3 driver name cstring", "test_m2_ch02_video_driver_name.py"),
    ]
    if args.include_ch01:
        tasks.insert(0, ("Chapter 1 regression", "run_m2_ch01_native_batch_v2.py"))
    results = []
    for label, script in tasks:
        print("\n===", label, "===", flush=True)
        path = ROOT / "tests" / script
        if not path.is_file():
            print("BLOCKED: missing", path)
            results.append((label, "BLOCKED"))
            continue
        command = [sys.executable, str(path), "--sdk", str(sdk)]
        if args.library and script != "run_m2_ch01_native_batch_v2.py":
            command += ["--library", str(args.library.expanduser().resolve())]
        try:
            proc = subprocess.run(command, text=True, capture_output=True, timeout=180, cwd=ROOT)
        except subprocess.TimeoutExpired:
            print("FAIL: timeout")
            results.append((label, "FAIL"))
            continue
        print(proc.stdout, end="")
        if proc.stderr:
            print(proc.stderr, file=sys.stderr, end="")
        status = "PASS" if proc.returncode == 0 else "BLOCKED" if proc.returncode == 2 else "FAIL"
        results.append((label, status))
    print("\n=== QGF MARATHON 2 CHAPTER 2 SUMMARY ===")
    for label, status in results:
        print(f"{status}: {label}")
    return 1 if any(s == "FAIL" for _, s in results) else 2 if any(s == "BLOCKED" for _, s in results) else 0

if __name__ == "__main__":
    sys.exit(main())
