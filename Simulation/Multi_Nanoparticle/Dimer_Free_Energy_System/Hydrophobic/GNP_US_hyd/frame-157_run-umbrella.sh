#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf157.gro -r conf157.gro -p insane.top -n index.ndx -o npt157.tpr -maxwarn 10
gmx mdrun -deffnm npt157 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt157.gro -r npt157.gro -t npt157.cpt -p insane.top -n index.ndx -o umbrella157.tpr -maxwarn 10
gmx mdrun -deffnm umbrella157 -nb gpu -v 
