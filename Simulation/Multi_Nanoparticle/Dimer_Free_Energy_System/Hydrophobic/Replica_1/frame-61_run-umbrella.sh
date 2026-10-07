#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf61.gro -r conf61.gro -p insane.top -n index.ndx -o npt61.tpr -maxwarn 10
gmx mdrun -deffnm npt61 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt61.gro -r npt61.gro -t npt61.cpt -p insane.top -n index.ndx -o umbrella61.tpr -maxwarn 10
gmx mdrun -deffnm umbrella61 -nb gpu -v 
