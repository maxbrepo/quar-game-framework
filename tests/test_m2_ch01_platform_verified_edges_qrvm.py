"""Exercise Core verified-prepare edge cases without native dependencies."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SDK = Path(os.environ.get("QUAR_SDK", str(ROOT / "sdk"))).expanduser().resolve()
SOURCES = (
    ROOT / "core/platform.vq",
    ROOT / "experimental/marathon2/chapter01/qgf_platform_verified_edges_probe.vq",
)
EXPECTED = [
    "true", "1", "false", "false", "0", "false", "0",
    "true", "1", "false", "2", "false", "3", "false",
    "0", "false", "false", "false", "false", "false", "false",
]


def main():
    if not (SDK / "main.py").is_file():
        print("BLOCKED: external SDK missing")
        return 2
    missing = [str(p.relative_to(ROOT)) for p in SOURCES if not p.is_file()]
    if missing:
        print("BLOCKED: missing sources:", ", ".join(missing))
        return 2
    program = "\n".join(
        line for path in SOURCES
        for line in path.read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("//")
    )
    with tempfile.TemporaryDirectory(prefix="qgf_cp25_") as temp:
        source = Path(temp) / "verified_edges.vq"
        source.write_text(program, encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, str(SDK / "main.py"), "-f", str(source)],
                cwd=SDK, input="1\n", capture_output=True, text=True, timeout=45,
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
        print("FAIL: verified prepare edge matrix")
        print("Expected:", EXPECTED)
        print("Observed:", observed)
        return 1
    print("PASS: Core verified prepare edge cases 21/21")
    return 0


if __name__ == "__main__":
    sys.exit(main())
