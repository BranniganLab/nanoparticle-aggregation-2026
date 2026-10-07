#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf687.gro -r conf687.gro -p insane.top -n index.ndx -o npt687.tpr -maxwarn 10
gmx mdrun -deffnm npt687 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt687.gro -r npt687.gro -t npt687.cpt -p insane.top -n index.ndx -o umbrella687.tpr -maxwarn 10
gmx mdrun -deffnm umbrella687 -nb gpu -v 
