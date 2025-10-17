#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c confXXX.gro -r confXXX.gro -p insane.top -n index.ndx -o nptXXX.tpr -maxwarn 10
gmx mdrun -deffnm nptXXX -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c nptXXX.gro -r nptXXX.gro -t nptXXX.cpt -p insane.top -n index.ndx -o umbrellaXXX.tpr -maxwarn 10
gmx mdrun -deffnm umbrellaXXX -nb gpu -v 
