#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf649.gro -r conf649.gro -p insane.top -n index.ndx -o npt649.tpr -maxwarn 10
gmx mdrun -deffnm npt649 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt649.gro -r npt649.gro -t npt649.cpt -p insane.top -n index.ndx -o umbrella649.tpr -maxwarn 10
gmx mdrun -deffnm umbrella649 -nb gpu -v 
