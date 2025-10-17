#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf191.gro -r conf191.gro -p insane.top -n index.ndx -o npt191.tpr -maxwarn 10
gmx mdrun -deffnm npt191 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt191.gro -r npt191.gro -t npt191.cpt -p insane.top -n index.ndx -o umbrella191.tpr -maxwarn 10
gmx mdrun -deffnm umbrella191 -nb gpu -v 
