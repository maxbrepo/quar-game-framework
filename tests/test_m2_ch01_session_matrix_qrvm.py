"""Exhaustive 4x4 matrix of the five canonical session predicates."""
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
    ROOT / "experimental/marathon2/chapter01/qgf_session_matrix_probe.vq",
)


def expected_values():
    results = []
    for app in range(4):
        for backend in range(4):
            results.extend([
                str(app == 0 and backend == 1).lower(),
                str(app == 1 and backend == 1).lower(),
                str(app in (1, 2) and backend in (1, 2)).lower(),
                str(app == 2 and backend == 2).lower(),
                str(app == 3 and backend == 3).lower(),
            ])
    return results


def main():
    if not (SDK / "main.py").is_file() or any(not p.is_file() for p in SOURCES):
        print("BLOCKED: SDK or QGF sources missing")
        return 2
    source_text = "\n".join(
        line for path in SOURCES
        for line in path.read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("//")
    )
    with tempfile.TemporaryDirectory(prefix="qgf_cp29_") as temp:
        path = Path(temp) / "session_matrix.vq"
        path.write_text(source_text, encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, str(SDK / "main.py"), "-f", str(path)],
                cwd=SDK, input="1\n", capture_output=True, text=True, timeout=60,
            )
        except subprocess.TimeoutExpired:
            print("FAIL: QRVM timeout")
            return 1
    if result.returncode or "=== QRVM OUTPUT ===" not in result.stdout or "Program executed successfully" not in result.stdout:
        print("FAIL: QRVM execution", result.stdout, result.stderr)
        return 1
    output = result.stdout.split("=== QRVM OUTPUT ===", 1)[1].split("Program executed successfully", 1)[0]
    actual = [line.strip().lower() for line in output.splitlines() if line.strip()]
    expected = expected_values()
    if actual != expected:
        mismatch = next(((i, a, e) for i, (a, e) in enumerate(zip(actual, expected)) if a != e), None)
        print("FAIL: session matrix", len(actual), "of", len(expected), "first mismatch", mismatch)
        return 1
    print("PASS: session coordination matrix 80/80 (16 state pairs x 5 predicates)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
