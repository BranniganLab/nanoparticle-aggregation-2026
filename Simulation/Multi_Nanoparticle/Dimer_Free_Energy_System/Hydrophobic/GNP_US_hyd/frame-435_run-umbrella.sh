#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf435.gro -r conf435.gro -p insane.top -n index.ndx -o npt435.tpr -maxwarn 10
gmx mdrun -deffnm npt435 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt435.gro -r npt435.gro -t npt435.cpt -p insane.top -n index.ndx -o umbrella435.tpr -maxwarn 10
gmx mdrun -deffnm umbrella435 -nb gpu -v 
