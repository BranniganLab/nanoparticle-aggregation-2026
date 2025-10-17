#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf584.gro -r conf584.gro -p insane.top -n index.ndx -o npt584.tpr -maxwarn 10
gmx mdrun -deffnm npt584 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt584.gro -r npt584.gro -t npt584.cpt -p insane.top -n index.ndx -o umbrella584.tpr -maxwarn 10
gmx mdrun -deffnm umbrella584 -nb gpu -v 
