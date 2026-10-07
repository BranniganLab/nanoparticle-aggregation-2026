#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf307.gro -r conf307.gro -p insane.top -n index.ndx -o npt307.tpr -maxwarn 10
gmx mdrun -deffnm npt307 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt307.gro -r npt307.gro -t npt307.cpt -p insane.top -n index.ndx -o umbrella307.tpr -maxwarn 10
gmx mdrun -deffnm umbrella307 -nb gpu -v 
