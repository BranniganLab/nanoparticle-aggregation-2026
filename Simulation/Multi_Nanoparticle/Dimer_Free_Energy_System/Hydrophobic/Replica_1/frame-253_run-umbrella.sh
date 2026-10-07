#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf253.gro -r conf253.gro -p insane.top -n index.ndx -o npt253.tpr -maxwarn 10
gmx mdrun -deffnm npt253 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt253.gro -r npt253.gro -t npt253.cpt -p insane.top -n index.ndx -o umbrella253.tpr -maxwarn 10
gmx mdrun -deffnm umbrella253 -nb gpu -v 
