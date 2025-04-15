#!/bin/bash
#SBATCH --job-name=vasp
#SBATCH -N 1
#SBATCH -n 48
#SBATCH -t 360
#SBATCH -o vasp.out
#SBATCH -e vasp.err
#SBATCH -p workq
#SBATCH -A loni_toghrul
#SBATCH --mail-type=END
#SBATCH --mail-user=ahill15@tulane.edu

source .venv/bin/activate

python src/chempipe/vasp.py
