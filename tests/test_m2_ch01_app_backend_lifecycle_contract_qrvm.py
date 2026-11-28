"""Verify that application and backend lifecycle policies remain distinct."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SDK = Path(os.environ.get("QUAR_SDK", str(ROOT / "sdk"))).expanduser().resolve()
DIRECTORY = ROOT / "experimental/marathon2/chapter01"
SOURCES = (
    ROOT / "core/lifecycle.vq",
    DIRECTORY / "qgf_lifecycle_transition.vq",
    DIRECTORY / "qgf_lifecycle_guard.vq",
    DIRECTORY / "qgf_lifecycle_sequence.vq",
    DIRECTORY / "qgf_lifecycle_contract.vq",
    DIRECTORY / "qgf_app_backend_lifecycle_bridge_probe.vq",
)
EXPECTED = [
    "true", "1", "true", "1", "1", "true", "2", "true",
    "0", "true", "2", "3", "0", "true", "false", "1",
]


def main():
    if not (SDK / "main.py").is_file():
        print("BLOCKED: Quar SDK missing")
        return 2
    missing = [str(path.relative_to(ROOT)) for path in SOURCES if not path.is_file()]
    if missing:
        print("BLOCKED: missing sources:", ", ".join(missing))
        return 2
    program = "\n".join(
        line for path in SOURCES
        for line in path.read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("//")
    )
    with tempfile.TemporaryDirectory(prefix="qgf_ch01_bridge_") as temp:
        source = Path(temp) / "bridge.vq"
        source.write_text(program, encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, str(SDK / "main.py"), "-f", str(source)],
                cwd=SDK, input="1\n", text=True, capture_output=True,
                timeout=45,
            )
        except subprocess.TimeoutExpired:
            print("FAIL: QRVM timed out")
            return 1
    if (result.returncode != 0 or "=== QRVM OUTPUT ===" not in result.stdout
            or "Program executed successfully" not in result.stdout):
        print("FAIL: QRVM execution")
        print(result.stdout)
        print(result.stderr)
        return 1
    output = result.stdout.split("=== QRVM OUTPUT ===", 1)[1]
    output = output.split("Program executed successfully", 1)[0]
    observed = [line.strip().lower() for line in output.splitlines() if line.strip()]
    if observed != EXPECTED:
        print("FAIL: application/backend lifecycle contract mismatch")
        print("Expected:", EXPECTED)
        print("Observed:", observed)
        return 1
    print("PASS: application/backend lifecycle separation and coordinated transitions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
