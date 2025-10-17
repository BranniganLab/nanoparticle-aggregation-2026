#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf72.gro -r conf72.gro -p insane.top -n index.ndx -o npt72.tpr -maxwarn 10
gmx mdrun -deffnm npt72 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt72.gro -r npt72.gro -t npt72.cpt -p insane.top -n index.ndx -o umbrella72.tpr -maxwarn 10
gmx mdrun -deffnm umbrella72 -nb gpu -v 
