#!/bin/bash
#SBATCH -J HexPR3
#SBATCH -o out%j.amarel.log 
#SBATCH --export=ALL
#SBATCH --partition=cmain
#SBATCH -N 1 -n 32
#SBATCH -t 72:00:00       # max time
#SBATCH --output=slurm.%N.%j.out     # STDOUT output file
#SBATCH --error=slurm.%N.%j.err      # STDERR output file (optional)
#SBATCH --requeue
#SBATCH --constraint=oarc

module load intel/17.0.1
module load mvapich2/2.2
module load cuda/8.0
module load gromacs/2016.1

SRUN1="srun -N 1 -n 1"
SRUN="srun -N 1 -n $SLURM_NTASKS --mpi=pmi2"

$SRUN1 gmx_mpi grompp -f ../../em.mdp -c insane.gro -p insane.top -o em -maxwarn 10
$SRUN1 gmx_mpi mdrun -ntomp 1 -deffnm em -v
$SRUN1 gmx_mpi grompp -f md_i.mdp -c em.gro -p insane.top -o md -maxwarn 10
$SRUN gmx_mpi mdrun -ntomp 1 -deffnm md -v -rdd 1.4
