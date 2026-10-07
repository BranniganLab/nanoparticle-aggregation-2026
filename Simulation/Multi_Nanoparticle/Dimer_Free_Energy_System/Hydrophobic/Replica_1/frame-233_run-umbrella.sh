#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf233.gro -r conf233.gro -p insane.top -n index.ndx -o npt233.tpr -maxwarn 10
gmx mdrun -deffnm npt233 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt233.gro -r npt233.gro -t npt233.cpt -p insane.top -n index.ndx -o umbrella233.tpr -maxwarn 10
gmx mdrun -deffnm umbrella233 -nb gpu -v 
