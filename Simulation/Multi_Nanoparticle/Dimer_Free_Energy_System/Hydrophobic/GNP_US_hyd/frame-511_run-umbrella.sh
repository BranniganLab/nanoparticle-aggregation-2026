#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf511.gro -r conf511.gro -p insane.top -n index.ndx -o npt511.tpr -maxwarn 10
gmx mdrun -deffnm npt511 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt511.gro -r npt511.gro -t npt511.cpt -p insane.top -n index.ndx -o umbrella511.tpr -maxwarn 10
gmx mdrun -deffnm umbrella511 -nb gpu -v 
