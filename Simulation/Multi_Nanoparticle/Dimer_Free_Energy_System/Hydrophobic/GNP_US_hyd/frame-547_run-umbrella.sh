#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf547.gro -r conf547.gro -p insane.top -n index.ndx -o npt547.tpr -maxwarn 10
gmx mdrun -deffnm npt547 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt547.gro -r npt547.gro -t npt547.cpt -p insane.top -n index.ndx -o umbrella547.tpr -maxwarn 10
gmx mdrun -deffnm umbrella547 -nb gpu -v 
