#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf555.gro -r conf555.gro -p insane.top -n index.ndx -o npt555.tpr -maxwarn 10
gmx mdrun -deffnm npt555 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt555.gro -r npt555.gro -t npt555.cpt -p insane.top -n index.ndx -o umbrella555.tpr -maxwarn 10
gmx mdrun -deffnm umbrella555 -nb gpu -v 
