#!/bin/bash

module unload mvapich2/2.3.3/intel-19.0.5
module load intel-mpi/2021.5.1
module load python/3.12.7-anaconda

TEST_MODE="${TEST_MODE:-false}"  # default to false if not set
converged="false"
iteration=0

while [ "$converged" = "false" ]; do
  echo "Starting iteration $iteration..."

  # Step 1: MatterSim relaxation
  sbatch --wait scripts/potential.sh

  # Step 2: VASP relaxation
  sbatch --wait scripts/vasp.sh

  # Step 3: Check convergence
  if [ -f status.json ]; then
    converged=$(jq -r .converged status.json)
    echo "Converged: $converged"
  else
    echo "status.json not found — exiting"
    exit 1
  fi

  # Simulate convergence after first iteration (test mode only)
  if [ "$TEST_MODE" = "true" ] && [ "$iteration" -ge 1 ]; then
    echo "TEST_MODE active: Forcing convergence = true"
    converged="true"
  fi

  # Step 4: Fine-tune if not converged
  if [ "$converged" = "false" ]; then
    echo "Fine-tuning MatterSim..."
    sbatch --wait scripts/fine_tune.sh
  else
    echo "DFT convergence achieved."
  fi

  iteration=$((iteration + 1))
done
