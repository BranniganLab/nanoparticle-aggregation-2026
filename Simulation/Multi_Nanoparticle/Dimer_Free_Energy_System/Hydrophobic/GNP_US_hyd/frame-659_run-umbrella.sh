#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf659.gro -r conf659.gro -p insane.top -n index.ndx -o npt659.tpr -maxwarn 10
gmx mdrun -deffnm npt659 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt659.gro -r npt659.gro -t npt659.cpt -p insane.top -n index.ndx -o umbrella659.tpr -maxwarn 10
gmx mdrun -deffnm umbrella659 -nb gpu -v 
