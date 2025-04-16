#!/bin/bash
#SBATCH --job-name=potential
#SBATCH -N 1
#SBATCH -n 24
#SBATCH -t 10
#SBATCH -o potential.out
#SBATCH -e potential.err
#SBATCH -p gpu
#SBATCH --gres=gpu:1
#SBATCH -A loni_username
#SBATCH --mail-type=END
#SBATCH --mail-user=username@tulane.edu

source .venv/bin/activate

python src/chempipe/potential.py
