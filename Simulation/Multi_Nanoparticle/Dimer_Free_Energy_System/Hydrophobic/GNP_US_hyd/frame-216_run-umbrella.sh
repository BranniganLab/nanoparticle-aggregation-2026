#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf216.gro -r conf216.gro -p insane.top -n index.ndx -o npt216.tpr -maxwarn 10
gmx mdrun -deffnm npt216 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt216.gro -r npt216.gro -t npt216.cpt -p insane.top -n index.ndx -o umbrella216.tpr -maxwarn 10
gmx mdrun -deffnm umbrella216 -nb gpu -v 
