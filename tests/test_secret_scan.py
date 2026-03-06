import subprocess
import tempfile
from pathlib import Path


def test_secret_scan_runs():

    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "example.txt"
        test_file.write_text("api_key = 'testkey123'")

        result = subprocess.run(
            ["python", "poc/sample-scripts/secret_scan.py", "--dir", tmpdir],
            capture_output=True,
            text=True
        )

        assert result.returncode in [0, 1]
