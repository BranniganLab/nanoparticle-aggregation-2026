#!/bin/bash
#SBATCH -J DODC8
#SBATCH --output=slurm.%N.%j.out     # STDOUT output file
#SBATCH --error=slurm.%N.%j.err      # STDERR output file (optional)
#SBATCH -o out%j.delta.log
#SBATCH --partition=gpuA100x4
#SBATCH --mem=50G
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1  # could be 1 for py-torch
#SBATCH --cpus-per-task=16   # spread out to use 1 core per numa, set to 64 if tasks is 1
#SBATCH --constraint="scratch"
#SBATCH --gpus-per-node=1
#SBATCH --account=bbyz-delta-gpu
#SBATCH --no-requeue
#SBATCH -t 48:00:00
#SBATCH --mail-user=jje63@scarletmail.rutgers.edu
#SBATCH --mail-type="BEGIN,END"

export OMP_NUM_THREADS=16
module load gromacs/2022.5.cuda
SRUN="srun -N $SLURM_NNODES -n $SLURM_NTASKS --mpi=pmi2"
SRUN1="srun -N 1 -n 1"

$SRUN1 gmx_mpi grompp -f ../../em.mdp -c insane.gro -p insane.top -o em -maxwarn 10
$SRUN1 gmx_mpi mdrun -deffnm em -v

$SRUN1 gmx_mpi grompp -f md_i.mdp -c em.gro -r em.gro -p insane.top -o md -maxwarn 10
$SRUN gmx_mpi mdrun -deffnm md -v -nb gpu -bonded gpu -update gpu

#srun gmx_mpi grompp -f md_i.mdp -c equil.gro -r equil.gro -p insane.top -o md -maxwarn 10
#srun gmx_mpi mdrun -deffnm md -v

