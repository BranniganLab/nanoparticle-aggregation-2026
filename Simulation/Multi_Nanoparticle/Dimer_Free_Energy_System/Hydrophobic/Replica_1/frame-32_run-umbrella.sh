#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf32.gro -r conf32.gro -p insane.top -n index.ndx -o npt32.tpr -maxwarn 10
gmx mdrun -deffnm npt32 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt32.gro -r npt32.gro -t npt32.cpt -p insane.top -n index.ndx -o umbrella32.tpr -maxwarn 10
gmx mdrun -deffnm umbrella32 -nb gpu -v 
