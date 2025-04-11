import subprocess
import json
import time
from pathlib import Path


def submit_and_wait(script_path: str) -> str:
    print(f"Submitting job: {script_path}")
    result = subprocess.run(
        ["sbatch", "--parsable", script_path], capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to submit job: {script_path}\n{result.stderr}")
    job_id = result.stdout.strip()
    print(f"Waiting for job {job_id} to finish...")
    subprocess.run(["scontrol", "wait", job_id])
    return job_id


def load_convergence_status(path="status.json") -> tuple[bool, str | None]:
    if not Path(path).exists():
        raise FileNotFoundError("No status.json found.")
    with open(path) as f:
        data = json.load(f)
    return data.get("converged", False), data.get("checkpoint", None)


def main():
    converged = False
    iteration = 0

    while not converged:
        print(f"\nStarting iteration {iteration}")

        # Step 1: MatterSim relaxation
        submit_and_wait("potential.sh")

        # Step 2: VASP relaxation
        submit_and_wait("vasp.sh")

        # Step 3: Check convergence
        try:
            converged, checkpoint = load_convergence_status()
            print(f"Converged: {converged}")
            if checkpoint:
                print(f"Checkpoint: {checkpoint}")
        except FileNotFoundError:
            print("No status.json found. Assuming failure.")
            break

        # Step 4: Fine-tune if not converged
        if not converged:
            print("Fine-tuning MatterSim...")
            submit_and_wait("fine_tune.sh")
        else:
            print("DFT convergence achieved.")

        iteration += 1
        time.sleep(2)


if __name__ == "__main__":
    main()
