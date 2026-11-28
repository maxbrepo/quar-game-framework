"""QRVM regression matrix for existing lifecycle contract; no SDL3 required."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SDK = Path(os.environ.get("QUAR_SDK", str(ROOT / "sdk"))).resolve()
DIRECTORY = ROOT / "experimental/marathon2/chapter01"
PARTS = ("qgf_lifecycle_transition.vq", "qgf_lifecycle_guard.vq",
         "qgf_lifecycle_sequence.vq", "qgf_lifecycle_contract.vq",
         "qgf_lifecycle_contract_matrix_probe.vq")


def expected_values():
    expected = []
    for state in (-1, 0, 1, 2, 3):
        for want in (True, False):
            for success in (True, False):
                action = 0
                if state == 0 and want:
                    action = 1
                elif state == 1 and not want:
                    action = 2
                elif state == 2 and not want:
                    action = 3
                after = state
                if action == 1:
                    after = 1 if success else 2
                elif action in (2, 3):
                    after = 0
                # The contract rejects invalid source states even for idle action.
                verified = state in (0, 1, 2)
                expected.extend((str(action), str(after), str(verified).lower()))
    return expected


def main():
    if not (SDK / "main.py").is_file():
        print("BLOCKED: external Quar SDK missing")
        return 2
    source = "\n".join(
        line for name in PARTS
        for line in (DIRECTORY / name).read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("//")
    )
    try:
        with tempfile.TemporaryDirectory(prefix="qgf_contract_matrix_") as temp:
            program = Path(temp) / "matrix.vq"
            program.write_text(source, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SDK / "main.py"), "-f", str(program)],
                cwd=SDK, input="1\n", capture_output=True, text=True,
                timeout=45,
            )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print("FAIL:", exc)
        return 1
    if result.returncode or "=== QRVM OUTPUT ===" not in result.stdout or "Program executed successfully" not in result.stdout:
        print("FAIL: QRVM execution")
        print(result.stdout)
        print(result.stderr)
        return 1
    output = result.stdout.split("=== QRVM OUTPUT ===", 1)[1].split("Program executed successfully", 1)[0]
    observed = [line.strip().lower() for line in output.splitlines() if line.strip()]
    expected = expected_values()
    if observed != expected:
        print("FAIL: contract matrix mismatch")
        for i, (actual, wanted) in enumerate(zip(observed, expected)):
            if actual != wanted:
                print("First mismatch at output", i, "expected", wanted, "actual", actual)
                break
        print("Observed output count:", len(observed), "expected:", len(expected))
        return 1
    print("PASS: QGF Lifecycle contract matrix 20/20 cases (QRVM typed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
