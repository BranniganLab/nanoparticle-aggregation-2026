#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf188.gro -r conf188.gro -p insane.top -n index.ndx -o npt188.tpr -maxwarn 10
gmx mdrun -deffnm npt188 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt188.gro -r npt188.gro -t npt188.cpt -p insane.top -n index.ndx -o umbrella188.tpr -maxwarn 10
gmx mdrun -deffnm umbrella188 -nb gpu -v 
