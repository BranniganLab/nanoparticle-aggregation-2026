#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf89.gro -r conf89.gro -p insane.top -n index.ndx -o npt89.tpr -maxwarn 10
gmx mdrun -deffnm npt89 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt89.gro -r npt89.gro -t npt89.cpt -p insane.top -n index.ndx -o umbrella89.tpr -maxwarn 10
gmx mdrun -deffnm umbrella89 -nb gpu -v 
