#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf629.gro -r conf629.gro -p insane.top -n index.ndx -o npt629.tpr -maxwarn 10
gmx mdrun -deffnm npt629 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt629.gro -r npt629.gro -t npt629.cpt -p insane.top -n index.ndx -o umbrella629.tpr -maxwarn 10
gmx mdrun -deffnm umbrella629 -nb gpu -v 
