#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf116.gro -r conf116.gro -p insane.top -n index.ndx -o npt116.tpr -maxwarn 10
gmx mdrun -deffnm npt116 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt116.gro -r npt116.gro -t npt116.cpt -p insane.top -n index.ndx -o umbrella116.tpr -maxwarn 10
gmx mdrun -deffnm umbrella116 -nb gpu -v 
