#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf274.gro -r conf274.gro -p insane.top -n index.ndx -o npt274.tpr -maxwarn 10
gmx mdrun -deffnm npt274 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt274.gro -r npt274.gro -t npt274.cpt -p insane.top -n index.ndx -o umbrella274.tpr -maxwarn 10
gmx mdrun -deffnm umbrella274 -nb gpu -v 
