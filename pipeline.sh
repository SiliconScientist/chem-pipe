#!/bin/bash
#SBATCH --job-name=chempipe
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 480
#SBATCH -p standard
#SBATCH -A loni_toghrul
#SBATCH -o pipeline.out
#SBATCH -e pipeline.err
#SBATCH --mail-type=END
#SBATCH --mail-user=ahill15@tulane.edu

source .venv/bin/activate
python -m chempipe