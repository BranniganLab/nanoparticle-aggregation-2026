#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf415.gro -r conf415.gro -p insane.top -n index.ndx -o npt415.tpr -maxwarn 10
gmx mdrun -deffnm npt415 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt415.gro -r npt415.gro -t npt415.cpt -p insane.top -n index.ndx -o umbrella415.tpr -maxwarn 10
gmx mdrun -deffnm umbrella415 -nb gpu -v 
