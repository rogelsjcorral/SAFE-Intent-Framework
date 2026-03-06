import subprocess

def test_enumeration_runs():
    result = subprocess.run(
        ["python", "poc/sample-scripts/enumerate_targets.py"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert len(result.stdout.strip()) > 0
