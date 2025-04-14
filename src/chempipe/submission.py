import json
import subprocess
from pathlib import Path


def submit_and_wait(script_path: str) -> str:
    print(f"Submitting job: {script_path}")
    result = subprocess.run(
        args=["sbatch", script_path],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to submit job: {script_path}\n{result.stderr}")
    job_id = result.stdout.strip()
    print(f"Waiting for job {job_id} to finish...")
    subprocess.run(["scontrol", "wait", job_id])
    return job_id


def load_convergence_status(path="status.json") -> bool:
    if not Path(path).exists():
        raise FileNotFoundError("No status.json found.")
    with open(path) as f:
        data = json.load(f)
    return data.get("converged", False)
