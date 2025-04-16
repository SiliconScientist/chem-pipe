#!/bin/bash
#SBATCH --job-name=chem-pipe
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 04:00:00
#SBATCH -p single
#SBATCH -A loni_toghrul
#SBATCH -o logs/pipeline_driver.out
#SBATCH -e logs/pipeline_driver.err
#SBATCH --mail-type=END
#SBATCH --mail-user=ahill15@tulane.edu

bash pipeline.sh