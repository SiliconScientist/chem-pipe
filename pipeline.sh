#!/bin/bash
#SBATCH --job-name=chempipe
#SBATCH -N 1
#SBATCH -n 32
#SBATCH -t 10
#SBATCH -o output.out
#SBATCH -e error.err
#SBATCH -p single
########SBATCH --gres=gpu:1
#SBATCH -A loni_hajar01
#SBATCH --mail-type=END
#SBATCH --mail-user=hhosseinifaradonbeh@tulane.edu

module purge
module load intel-mpi/2021.5.1
module load python/3.12.7-anaconda

source .venv/bin/activate

TEST_MODE="${TEST_MODE:-false}"  # default to false if not set
converged="false"
iteration=0
SECONDS=0

while [ "$converged" = "false" ]; do
  echo "Starting iteration $iteration..."

  # Step 1: MatterSim relaxation
  python src/chempipe/potential.py

  # Step 2: VASP relaxation
  python src/chempipe/vasp.py

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
    export LOCAL_RANK=0
    python src/chempipe/fine_tune.py
  else
    duration=$SECONDS
    printf -v hhmmss '%02d:%02d:%02d' $((duration/3600)) $((duration%3600/60)) $((duration%60))
    echo "DFT convergence achieved in $hhmmss (HH:MM:SS)."
  fi

  iteration=$((iteration + 1))
done
export LOCAL_RANK=0 # needed or mattersim fine tuning gives an error                           
export RANK=0
export WORLD_SIZE=1
export MASTER_ADDR="127.0.0.1"
export MASTER_PORT="12345"
