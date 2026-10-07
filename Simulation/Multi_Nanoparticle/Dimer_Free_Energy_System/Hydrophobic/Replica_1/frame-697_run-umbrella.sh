#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf697.gro -r conf697.gro -p insane.top -n index.ndx -o npt697.tpr -maxwarn 10
gmx mdrun -deffnm npt697 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt697.gro -r npt697.gro -t npt697.cpt -p insane.top -n index.ndx -o umbrella697.tpr -maxwarn 10
gmx mdrun -deffnm umbrella697 -nb gpu -v 
