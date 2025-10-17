#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf0.gro -r conf0.gro -p insane.top -n index.ndx -o npt0.tpr -maxwarn 10
gmx mdrun -deffnm npt0 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt0.gro -r npt0.gro -t npt0.cpt -p insane.top -n index.ndx -o umbrella0.tpr -maxwarn 10
gmx mdrun -deffnm umbrella0 -nb gpu -v 
