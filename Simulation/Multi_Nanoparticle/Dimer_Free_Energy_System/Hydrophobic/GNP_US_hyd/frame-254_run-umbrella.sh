#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf254.gro -r conf254.gro -p insane.top -n index.ndx -o npt254.tpr -maxwarn 10
gmx mdrun -deffnm npt254 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt254.gro -r npt254.gro -t npt254.cpt -p insane.top -n index.ndx -o umbrella254.tpr -maxwarn 10
gmx mdrun -deffnm umbrella254 -nb gpu -v 
