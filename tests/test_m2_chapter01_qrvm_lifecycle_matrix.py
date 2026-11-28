"""Execute the real QGF typed lifecycle implementation through the bundled external QRVM."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "core/lifecycle.vq"
PROBE = ROOT / "experimental/marathon2/chapter01/qgf_core_lifecycle_matrix_qrvm.vq"
EXPECTED = ['1', '0', '0', '1', '0', '1', '1', '1', '2', '0', '3', '0', '2', '1', '2', '1', '3', '0', '3', '1', '3', '1', '3', '1']


class CoreLifecycleQrvmMatrix(unittest.TestCase):
    def test_typed_lifecycle_matrix_through_qrvm(self):
        sdk = Path(os.environ.get("QUAR_SDK", str(ROOT / "sdk"))).expanduser().resolve()
        self.assertTrue((sdk / "main.py").is_file(), "Quar SDK missing; install external SDK in sdk/ or set QUAR_SDK")
        with tempfile.TemporaryDirectory(prefix="qgf_lifecycle_qrvm_") as directory:
            source = Path(directory) / "matrix.vq"
            source.write_text("\n".join(line for line in (MODULE.read_text(encoding="utf-8") + "\n" + PROBE.read_text(encoding="utf-8")).splitlines() if not line.lstrip().startswith("//")), encoding="utf-8")
            result = subprocess.run([sys.executable, str(sdk / "main.py"), "-f", str(source)],
                                    cwd=sdk, input="1\n", capture_output=True, text=True,
                                    timeout=45, env={**os.environ, "TERM": "dumb"})
        self.assertEqual(result.returncode, 0, result.stdout + "\n" + result.stderr)
        self.assertIn("=== QRVM OUTPUT ===", result.stdout, result.stdout)
        self.assertIn("Program executed successfully", result.stdout, result.stdout)
        output = result.stdout.split("=== QRVM OUTPUT ===", 1)[1].split("Program executed successfully", 1)[0]
        actual = [line.strip() for line in output.splitlines() if line.strip()]
        self.assertEqual(actual, EXPECTED)


if __name__ == "__main__":
    unittest.main()
