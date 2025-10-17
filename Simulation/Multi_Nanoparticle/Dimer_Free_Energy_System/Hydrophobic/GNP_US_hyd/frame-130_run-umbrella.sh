#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf130.gro -r conf130.gro -p insane.top -n index.ndx -o npt130.tpr -maxwarn 10
gmx mdrun -deffnm npt130 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt130.gro -r npt130.gro -t npt130.cpt -p insane.top -n index.ndx -o umbrella130.tpr -maxwarn 10
gmx mdrun -deffnm umbrella130 -nb gpu -v 
