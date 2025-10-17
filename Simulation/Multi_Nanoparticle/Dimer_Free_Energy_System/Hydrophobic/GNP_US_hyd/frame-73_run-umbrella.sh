#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf73.gro -r conf73.gro -p insane.top -n index.ndx -o npt73.tpr -maxwarn 10
gmx mdrun -deffnm npt73 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt73.gro -r npt73.gro -t npt73.cpt -p insane.top -n index.ndx -o umbrella73.tpr -maxwarn 10
gmx mdrun -deffnm umbrella73 -nb gpu -v 
