import time

from chempipe.submission import submit_and_wait, load_convergence_status


def main():
    converged = False
    iteration = 0
    while not converged:
        print(f"\nStarting iteration {iteration}")
        print("Running potential.sh...")
        submit_and_wait("potential.sh")

        print("Running vasp.sh...")
        submit_and_wait("vasp.sh")
        try:
            converged = load_convergence_status()
        except FileNotFoundError:
            print("No status.json found. Assuming failure.")
            break
        if converged:
            print("DFT convergence achieved.")
        else:
            submit_and_wait("fine_tune.sh")

        iteration += 1
        time.sleep(2)


if __name__ == "__main__":
    main()
