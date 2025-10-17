#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf431.gro -r conf431.gro -p insane.top -n index.ndx -o npt431.tpr -maxwarn 10
gmx mdrun -deffnm npt431 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt431.gro -r npt431.gro -t npt431.cpt -p insane.top -n index.ndx -o umbrella431.tpr -maxwarn 10
gmx mdrun -deffnm umbrella431 -nb gpu -v 
