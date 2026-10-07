#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf678.gro -r conf678.gro -p insane.top -n index.ndx -o npt678.tpr -maxwarn 10
gmx mdrun -deffnm npt678 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt678.gro -r npt678.gro -t npt678.cpt -p insane.top -n index.ndx -o umbrella678.tpr -maxwarn 10
gmx mdrun -deffnm umbrella678 -nb gpu -v 
