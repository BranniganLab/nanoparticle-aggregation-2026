#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf334.gro -r conf334.gro -p insane.top -n index.ndx -o npt334.tpr -maxwarn 10
gmx mdrun -deffnm npt334 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt334.gro -r npt334.gro -t npt334.cpt -p insane.top -n index.ndx -o umbrella334.tpr -maxwarn 10
gmx mdrun -deffnm umbrella334 -nb gpu -v 
