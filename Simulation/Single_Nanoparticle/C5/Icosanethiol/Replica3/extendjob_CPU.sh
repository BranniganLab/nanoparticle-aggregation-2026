#!/bin/bash
#SBATCH -J C5IR3
#SBATCH -o out%j.amarel.log 
#SBATCH --export=ALL
#SBATCH --partition=cmain
#SBATCH -N 1 -n 32
#SBATCH -t 72:00:00       # max time
#SBATCH --output=slurm.%N.%j.out     # STDOUT output file
#SBATCH --error=slurm.%N.%j.err      # STDERR output file (optional)
#SBATCH --requeue

module load apptainer/1.2.5

srun apptainer run -B /scratch/${USER}:/scratch/${USER} --nv /projects/community/singularity.images/GROMACS/gromacs_2023.2_GPU.sif \
	gmx mdrun -ntmpi 1 -cpi production/md1.cpi -deffnm production/md1 -v
