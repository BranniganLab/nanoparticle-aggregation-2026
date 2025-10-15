#!/bin/bash
#SBATCH -J OctPR6
#SBATCH -o out%j.amarel.log
#SBATCH --partition=cgpu 
#SBATCH --export=ALL
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=25
#SBATCH --constraint=ampere
#SBATCH -t 72:00:00       # max time
#SBATCH --output=slurm.%N.%j.out     # STDOUT output file
#SBATCH --error=slurm.%N.%j.err      # STDERR output file (optional)

module load intel/17.0.1
module load mvapich2/2.2
module load cuda/8.0
module load gromacs/2016.1

#SRUN1="srun -N 1 -n 1"
SRUN="srun --mpi=pmi2"

$SRUN gmx_mpi grompp -f ../../em.mdp -c insane.gro -p insane.top -o em -maxwarn 10
$SRUN gmx_mpi mdrun -ntomp 1 -deffnm em -v
$SRUN gmx_mpi grompp -f md_i.mdp -c em.gro -p insane.top -o md -maxwarn 10
$SRUN gmx_mpi mdrun -ntomp 1 -deffnm md -v -rdd 1.4
