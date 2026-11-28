"""Platform configuration and error precedence matrix."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SDK = Path(os.environ.get("QUAR_SDK", str(ROOT / "sdk"))).expanduser().resolve()
CORE = ROOT / "core/platform.vq"
PROBE = ROOT / "experimental/marathon2/chapter03/qgf_platform_config_probe.vq"
EXPECTED = ['false', '1', 'false', '1', 'false', '1', 'false', '1', 'false', '1', 'false', '1', 'false', '1', 'false', '1', 'false', '2', 'true', '0', 'true', '3', 'false', '2', 'false', '2', 'true', '0', 'true', '3', 'false', '2', 'false', '2', 'true', '0', 'true', '3', 'false', '2', 'false', '2', 'true', '0', 'true', '3', 'false', '2', 'false', '1', 'false', '1', 'false', '1', 'false', '1']


def main():
    if not (SDK / "main.py").is_file():
        print("BLOCKED: external Quar SDK missing")
        return 2
    if not CORE.is_file() or not PROBE.is_file():
        print("BLOCKED: platform sources missing")
        return 2
    source = "\n".join(
        line for path in (CORE, PROBE)
        for line in path.read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("//")
    )
    with tempfile.TemporaryDirectory(prefix="qgf_ch01_platform_matrix_") as tmp:
        path = Path(tmp) / "platform_matrix.vq"
        path.write_text(source, encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, str(SDK / "main.py"), "-f", str(path)],
                cwd=SDK, input="1\n", capture_output=True, text=True, timeout=60,
            )
        except subprocess.TimeoutExpired:
            print("FAIL: QRVM timeout")
            return 1
    if (result.returncode != 0 or "=== QRVM OUTPUT ===" not in result.stdout
            or "Program executed successfully" not in result.stdout):
        print("FAIL: QRVM execution")
        print(result.stdout)
        print(result.stderr)
        return 1
    payload = result.stdout.split("=== QRVM OUTPUT ===", 1)[1]
    payload = payload.split("Program executed successfully", 1)[0]
    observed = [line.strip().lower() for line in payload.splitlines() if line.strip()]
    if observed != EXPECTED:
        for index, (actual, wanted) in enumerate(zip(observed, EXPECTED)):
            if actual != wanted:
                print("FAIL: first mismatch at", index, "expected", wanted, "actual", actual)
                break
        print("Output counts:", len(observed), len(EXPECTED))
        return 1
    print("PASS: CP02 platform configuration matrix %d/%d checks" % (len(EXPECTED), len(EXPECTED)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
