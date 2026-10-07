#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf242.gro -r conf242.gro -p insane.top -n index.ndx -o npt242.tpr -maxwarn 10
gmx mdrun -deffnm npt242 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt242.gro -r npt242.gro -t npt242.cpt -p insane.top -n index.ndx -o umbrella242.tpr -maxwarn 10
gmx mdrun -deffnm umbrella242 -nb gpu -v 
