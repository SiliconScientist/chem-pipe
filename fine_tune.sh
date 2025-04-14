#!/bin/bash
#SBATCH --job-name=fine_tune
#SBATCH -N 1
#SBATCH -n 24
#SBATCH -t 10
#SBATCH -o fine_tune.out
#SBATCH -e fine_tune.err
#SBATCH -p gpu
#SBATCH --gres=gpu:1
#SBATCH -A loni_toghrul
#SBATCH --mail-type=END
#SBATCH --mail-user=ahill15@tulane.edu

torchrun --nproc_per_node=1 src/chempipe/fine_tune.py
