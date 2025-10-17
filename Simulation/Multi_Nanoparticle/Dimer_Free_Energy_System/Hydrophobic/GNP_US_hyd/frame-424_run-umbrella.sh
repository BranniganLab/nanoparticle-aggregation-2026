#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf424.gro -r conf424.gro -p insane.top -n index.ndx -o npt424.tpr -maxwarn 10
gmx mdrun -deffnm npt424 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt424.gro -r npt424.gro -t npt424.cpt -p insane.top -n index.ndx -o umbrella424.tpr -maxwarn 10
gmx mdrun -deffnm umbrella424 -nb gpu -v 
