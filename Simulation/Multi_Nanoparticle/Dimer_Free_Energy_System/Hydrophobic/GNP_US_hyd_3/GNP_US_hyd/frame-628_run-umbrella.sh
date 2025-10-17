#!/bin/bash

#SBATCH -J US628
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
	gmx grompp -f npt_umbrella.mdp -c conf628.gro -r conf628.gro -p insane.top -n index.ndx -o npt628.tpr -maxwarn 10

srun apptainer run -B /scratch/${USER}:/scratch/${USER} --nv /projects/community/singularity.images/GROMACS/gromacs_2023.2_GPU.sif \
	gmx mdrun -ntmpi 1 -nb gpu -deffnm npt628 -v

# Umbrella run

srun apptainer run -B /scratch/${USER}:/scratch/${USER} --nv /projects/community/singularity.images/GROMACS/gromacs_2023.2_GPU.sif \
	gmx grompp -f md_umbrella.mdp -c npt628.gro -r npt628.gro -t npt628.cpt -p insane.top -n index.ndx -o umbrella628.tpr -maxwarn 10

srun apptainer run -B /scratch/${USER}:/scratch/${USER} --nv /projects/community/singularity.images/GROMACS/gromacs_2023.2_GPU.sif \
	gmx mdrun -ntmpi 1 -nb gpu -deffnm umbrella628 -v 
