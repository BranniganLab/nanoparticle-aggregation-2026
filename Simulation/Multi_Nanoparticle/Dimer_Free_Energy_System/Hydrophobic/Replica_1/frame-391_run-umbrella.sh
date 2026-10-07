#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf391.gro -r conf391.gro -p insane.top -n index.ndx -o npt391.tpr -maxwarn 10
gmx mdrun -deffnm npt391 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt391.gro -r npt391.gro -t npt391.cpt -p insane.top -n index.ndx -o umbrella391.tpr -maxwarn 10
gmx mdrun -deffnm umbrella391 -nb gpu -v 
