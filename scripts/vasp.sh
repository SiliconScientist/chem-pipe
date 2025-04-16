#!/bin/bash
#SBATCH --job-name=vasp
#SBATCH -N 1
#SBATCH -n 48
#SBATCH -t 360
#SBATCH -o vasp.out
#SBATCH -e vasp.err
#SBATCH -p workq
#SBATCH -A loni_username
#SBATCH --mail-type=END
#SBATCH --mail-user=username@tulane.edu

source .venv/bin/activate

python src/chempipe/vasp.py
