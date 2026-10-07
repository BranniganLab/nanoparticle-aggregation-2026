#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf102.gro -r conf102.gro -p insane.top -n index.ndx -o npt102.tpr -maxwarn 10
gmx mdrun -deffnm npt102 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt102.gro -r npt102.gro -t npt102.cpt -p insane.top -n index.ndx -o umbrella102.tpr -maxwarn 10
gmx mdrun -deffnm umbrella102 -nb gpu -v 
