"""Verify native session entry and release guards in canonical QGF Core."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SDK = Path(os.environ.get("QUAR_SDK", str(ROOT / "sdk"))).resolve()
SOURCES = (
    ROOT / "core/lifecycle.vq",
    ROOT / "core/platform.vq",
    ROOT / "core/session.vq",
    ROOT / "experimental/marathon2/chapter01/qgf_session_entry_release_probe.vq",
)
EXPECTED = [
    "true", "false", "false", "false", "false", "false", "false", "false",
    "false", "true", "true", "true", "true", "false",
]


def main():
    if not (SDK / "main.py").is_file() or any(not p.is_file() for p in SOURCES):
        print("BLOCKED: SDK or QGF sources missing")
        return 2
    program = "\n".join(
        line for path in SOURCES
        for line in path.read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("//")
    )
    with tempfile.TemporaryDirectory(prefix="qgf_cp31_") as temp:
        source = Path(temp) / "session_guard.vq"
        source.write_text(program, encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, str(SDK / "main.py"), "-f", str(source)],
                cwd=SDK, input="1\n", text=True, capture_output=True, timeout=60,
            )
        except subprocess.TimeoutExpired:
            print("FAIL: QRVM timeout")
            return 1
    if result.returncode or "=== QRVM OUTPUT ===" not in result.stdout or "Program executed successfully" not in result.stdout:
        print("FAIL: QRVM execution")
        print(result.stdout)
        print(result.stderr)
        return 1
    payload = result.stdout.split("=== QRVM OUTPUT ===", 1)[1].split("Program executed successfully", 1)[0]
    observed = [line.strip().lower() for line in payload.splitlines() if line.strip()]
    if observed != EXPECTED:
        print("FAIL: session guards", "expected:", EXPECTED, "observed:", observed)
        return 1
    print("PASS: QGF Core session entry/release guards 14/14")
    return 0


if __name__ == "__main__":
    sys.exit(main())
