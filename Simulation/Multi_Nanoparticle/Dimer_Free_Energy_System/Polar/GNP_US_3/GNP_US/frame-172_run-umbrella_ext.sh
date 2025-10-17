#!/bin/bash

#SBATCH -J US172
#SBATCH -o out%j.amarel.log 
#SBATCH --export=ALL
#SBATCH --partition=cgpu
#SBATCH --gres=gpu:1
#SBATCH --ntasks=1
#SBATCH -t 72:00:00       # max time
#SBATCH --output=slurm.%N.%j.out     # STDOUT output file
#SBATCH --error=slurm.%N.%j.err      # STDERR output file (optional)
#SBATCH --no-requeue

module load apptainer/1.2.5

# Short equilibration

srun apptainer run -B /scratch/${USER}:/scratch/${USER} --nv /projects/community/singularity.images/GROMACS/gromacs_2023.2_GPU.sif \
	gmx mdrun -ntmpi 1 -cpi umbrella172.cpt -nb gpu -deffnm umbrella172 -px umbrella172_pullx -pf umbrella172_pullf -v 
