#!/bin/bash
#SBATCH -p workq
#SBATCH -A loni_toghrul
#SBATCH -p workq
#SBATCH -N 1
#SBATCH -n 64
#SBATCH -t 10
#SBATCH -o test_%j_%N.out
#SBATCH -e test_%j_%N.err
#SBATCH --mail-user=ahill15@tulane.edu
#SBATCH --mail-type=ALL

module unload mvapich2/2.3.3/intel-19.0.5
module load intel-mpi/2021.5.1
module load python/3.12.7-anaconda

TEST_MODE="${TEST_MODE:-false}"  # default to false if not set
converged="false"
iteration=0
SECONDS=0

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

if [ "$TEST_MODE" = "true" ] && [ "$iteration" -eq 0 ]; then
  echo "TEST_MODE active: Forcing convergence = false"
  converged="false"
fi

  # Step 4: Fine-tune if not converged
  if [ "$converged" = "false" ]; then
    echo "Fine-tuning MatterSim..."
    sbatch --wait scripts/fine_tune.sh
  else
    duration=$SECONDS
    printf -v hhmmss '%02d:%02d:%02d' $((duration/3600)) $((duration%3600/60)) $((duration%60))
    echo "DFT convergence achieved in $hhmmss (HH:MM:SS)."
  fi

  iteration=$((iteration + 1))
done
