import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "os_resource_sim", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def test_cli_schedule_json_success():
    result = run_cli("schedule", "--algorithm", "fcfs", "--input", "data/samples/scheduling.json")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["module"] == "scheduling"


def test_cli_invalid_quantum_exit_code():
    result = run_cli("schedule", "--algorithm", "rr", "--quantum", "0", "--input", "data/samples/scheduling.json")
    assert result.returncode == 2
    assert "ERROR:" in result.stdout


def test_cli_validate_csv_success():
    result = run_cli("validate", "--type", "storage", "--input", "data/samples/storage.csv")
    assert result.returncode == 0
    assert "VALID" in result.stdout


def test_cli_demo_writes_report(tmp_path: Path):
    out = tmp_path / "reports"
    result = run_cli("demo", "--root", ".", "--output-dir", str(out))
    assert result.returncode == 0
    assert (out / "demo_report.json").exists()
