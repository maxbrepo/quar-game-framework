"""Black-box QRVM smoke test; does not modify the Quar SDK."""
import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sdk", required=True, type=Path, help="Path to quar-sdk")
    args = parser.parse_args()
    sdk = args.sdk.resolve()
    if not (sdk / "main.py").exists():
        parser.error("SDK path must contain main.py")
    module_file = ROOT / "core" / "math" / "vector2.vq"
    test_file = ROOT / "examples" / "001_math" / "main.vq"
    # The current QRVM single-file path does not execute imports yet.
    # Assemble an ephemeral test program, keeping the library source canonical.
    import tempfile
    with tempfile.TemporaryDirectory(prefix="qgf_math_") as temporary:
        assembled = Path(temporary) / "math_test.vq"
        assembled.write_text(module_file.read_text() + "\n" + test_file.read_text(), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(sdk / "main.py"), "-f", str(assembled)],
            cwd=sdk,
            input="1\n",
            text=True,
            capture_output=True,
            timeout=30,
            env={**os.environ, "TERM": "dumb"},
        )
    print(result.stdout, end="")
    if result.returncode:
        print(result.stderr, file=sys.stderr)
        return result.returncode
    values = [line.strip() for line in result.stdout.splitlines() if line.strip() and line.strip() not in ("=== QRVM OUTPUT ===", "Program executed successfully") and not line.startswith(("Source:", "Execution mode:", "[1]", "[2]", "> "))]
    expected = [25.0, 11.0, -2.0, 25.0]
    try:
        numbers = [float(line) for line in values]
    except ValueError:
        print(f"Unexpected QRVM output: {values!r}", file=sys.stderr)
        return 1
    if numbers != expected:
        print(f"Expected {expected!r}, got {numbers!r}", file=sys.stderr)
        return 1
    print("QGF math smoke test: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
