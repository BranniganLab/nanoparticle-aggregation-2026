#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf553.gro -r conf553.gro -p insane.top -n index.ndx -o npt553.tpr -maxwarn 10
gmx mdrun -deffnm npt553 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt553.gro -r npt553.gro -t npt553.cpt -p insane.top -n index.ndx -o umbrella553.tpr -maxwarn 10
gmx mdrun -deffnm umbrella553 -nb gpu -v 
