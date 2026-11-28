"""Audit the public platform contract against the native SDL3 prototype status."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SDK = Path(os.environ.get("QUAR_SDK", str(ROOT / "sdk"))).expanduser().resolve()
CORE = ROOT / "core/platform.vq"
PROBE = ROOT / "experimental/marathon2/chapter01/qgf_platform_backend_contract_probe.vq"
EXPECTED = ["1", "true", "false", "true", "false", "3", "0",
            "false", "false", "false", "true", "3"]


def main():
    if not (SDK / "main.py").is_file():
        print("BLOCKED: external Quar SDK missing")
        return 2
    if not CORE.is_file() or not PROBE.is_file():
        print("BLOCKED: QGF platform contract sources missing")
        return 2
    source = "\n".join(
        line for file in (CORE, PROBE)
        for line in file.read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("//")
    )
    with tempfile.TemporaryDirectory(prefix="qgf_platform_contract_") as tmp:
        program = Path(tmp) / "platform_contract.vq"
        program.write_text(source, encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, str(SDK / "main.py"), "-f", str(program)],
                cwd=SDK, input="1\n", capture_output=True, text=True, timeout=45,
            )
        except subprocess.TimeoutExpired:
            print("FAIL: QRVM timeout")
            return 1
    if (result.returncode or "=== QRVM OUTPUT ===" not in result.stdout
            or "Program executed successfully" not in result.stdout):
        print("FAIL: QRVM execution")
        print(result.stdout)
        print(result.stderr)
        return 1
    payload = result.stdout.split("=== QRVM OUTPUT ===", 1)[1]
    payload = payload.split("Program executed successfully", 1)[0]
    observed = [line.strip().lower() for line in payload.splitlines() if line.strip()]
    if observed != EXPECTED:
        print("FAIL: platform contract changed; review before enabling SDL3")
        print("Expected:", EXPECTED)
        print("Observed:", observed)
        return 1
    print("PASS: public platform contract reserves SDL3 but does not advertise native availability")
    return 0


if __name__ == "__main__":
    sys.exit(main())
