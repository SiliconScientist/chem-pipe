#!/bin/bash
#SBATCH --job-name=chempipe
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 480
#SBATCH -p single
#SBATCH -A loni_toghrul
#SBATCH -o pipeline.out
#SBATCH -e pipeline.err
#SBATCH --mail-type=END
#SBATCH --mail-user=ahill15@tulane.edu

module unload mvapich2/2.3.3/intel-19.0.5
module load intel-mpi/2021.5.1
module load python/3.12.7-anaconda

converged=0
iteration=0

while [ $converged -eq 0 ]; do
  echo "Starting iteration $iteration..."

  # Step 1: MatterSim relaxation
  sbatch --wait scripts/potential.sh

  # Step 2: VASP relaxation
  sbatch --wait scripts/vasp.sh

  # Step 3: Check convergence
  if [ -f status.json ]; then
    converged=$(jq -r .converged status.json)
    echo "Converged: $converged"
    checkpoint=$(jq -r .checkpoint status.json)
    echo "Checkpoint: $checkpoint"
  else
    echo "status.json not found — exiting"
    exit 1
  fi

  # Step 4: Fine-tune if not converged
  if [ "$converged" -eq 0 ]; then
    echo "Fine-tuning MatterSim..."
    sbatch --wait scripts/fine_tune.sh
  else
    echo "DFT convergence achieved."
  fi

  iteration=$((iteration + 1))
done
