#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf408.gro -r conf408.gro -p insane.top -n index.ndx -o npt408.tpr -maxwarn 10
gmx mdrun -deffnm npt408 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt408.gro -r npt408.gro -t npt408.cpt -p insane.top -n index.ndx -o umbrella408.tpr -maxwarn 10
gmx mdrun -deffnm umbrella408 -nb gpu -v 
