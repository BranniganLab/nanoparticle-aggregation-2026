#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf520.gro -r conf520.gro -p insane.top -n index.ndx -o npt520.tpr -maxwarn 10
gmx mdrun -deffnm npt520 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt520.gro -r npt520.gro -t npt520.cpt -p insane.top -n index.ndx -o umbrella520.tpr -maxwarn 10
gmx mdrun -deffnm umbrella520 -nb gpu -v 
