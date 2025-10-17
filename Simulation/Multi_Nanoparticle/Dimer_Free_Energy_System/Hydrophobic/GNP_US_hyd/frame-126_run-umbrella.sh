#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf126.gro -r conf126.gro -p insane.top -n index.ndx -o npt126.tpr -maxwarn 10
gmx mdrun -deffnm npt126 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt126.gro -r npt126.gro -t npt126.cpt -p insane.top -n index.ndx -o umbrella126.tpr -maxwarn 10
gmx mdrun -deffnm umbrella126 -nb gpu -v 
