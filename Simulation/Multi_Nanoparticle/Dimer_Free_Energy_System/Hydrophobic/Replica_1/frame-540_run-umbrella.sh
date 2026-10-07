#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf540.gro -r conf540.gro -p insane.top -n index.ndx -o npt540.tpr -maxwarn 10
gmx mdrun -deffnm npt540 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt540.gro -r npt540.gro -t npt540.cpt -p insane.top -n index.ndx -o umbrella540.tpr -maxwarn 10
gmx mdrun -deffnm umbrella540 -nb gpu -v 
