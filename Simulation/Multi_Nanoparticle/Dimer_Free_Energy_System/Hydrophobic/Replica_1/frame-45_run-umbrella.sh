#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf45.gro -r conf45.gro -p insane.top -n index.ndx -o npt45.tpr -maxwarn 10
gmx mdrun -deffnm npt45 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt45.gro -r npt45.gro -t npt45.cpt -p insane.top -n index.ndx -o umbrella45.tpr -maxwarn 10
gmx mdrun -deffnm umbrella45 -nb gpu -v 
