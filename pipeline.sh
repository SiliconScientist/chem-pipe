#!/bin/bash

CONFIG_FILE="config.toml"
get_config_value() {
    grep -E "^$1\s*=" "$CONFIG_FILE" | head -n1 | cut -d '=' -f2- | sed 's/#.*//' | tr -d ' "' 
}

JOB_NAME=$(get_config_value "job_name")
ACCOUNT=$(get_config_value "account")
PARTITION=$(get_config_value "partition")
NODES=$(get_config_value "nodes")
NTASKS=$(get_config_value "ntasks")
TIME=$(get_config_value "time")
MAIL_USER=$(get_config_value "mail_user")
MAIL_TYPE=$(get_config_value "mail_type")

# Define your temporary job script
JOB_SCRIPT="temp.slurm"

# Write the job file
cat <<EOF > "$JOB_SCRIPT"
#!/bin/bash
#SBATCH --job-name=$JOB_NAME
#SBATCH --account=$ACCOUNT
#SBATCH --partition=$PARTITION
#SBATCH --nodes=$NODES
#SBATCH --ntasks=$NTASKS
#SBATCH --time=$TIME
#SBATCH --mail-user=$MAIL_USER
#SBATCH --mail-type=$MAIL_TYPE
#SBATCH --output=logs/%x_%j.out

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
EOF

# Submit the job
sbatch "$JOB_SCRIPT"
rm "$JOB_SCRIPT"