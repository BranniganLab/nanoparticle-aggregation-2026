#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf291.gro -r conf291.gro -p insane.top -n index.ndx -o npt291.tpr -maxwarn 10
gmx mdrun -deffnm npt291 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt291.gro -r npt291.gro -t npt291.cpt -p insane.top -n index.ndx -o umbrella291.tpr -maxwarn 10
gmx mdrun -deffnm umbrella291 -nb gpu -v 
