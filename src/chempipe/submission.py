import json
import time
import subprocess
from pathlib import Path


def submit_and_wait(script_path: str, poll_interval: int = 10) -> str:
    print(f"Submitting job: {script_path}")
    result = subprocess.run(
        f"sbatch {script_path}",
        shell=True,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"[ERROR] Failed to submit job:\n{result.stderr}")
    job_id = result.stdout.strip().split()[-1]
    print(f"Job {job_id} submitted. Waiting for it to finish...")
    while True:
        check = subprocess.run(
            f"squeue -j {job_id}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        if job_id not in check.stdout:
            print(f"Job {job_id} finished.")
            break
        time.sleep(poll_interval)
    subprocess.run("sync && sleep 2", shell=True)
    return job_id


def load_convergence_status(path="status.json") -> bool:
    if not Path(path).exists():
        raise FileNotFoundError("No status.json found.")
    with open(path) as f:
        data = json.load(f)
    return data.get("converged", False)
