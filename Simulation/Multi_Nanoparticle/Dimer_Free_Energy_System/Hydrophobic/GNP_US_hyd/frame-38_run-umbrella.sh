#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf38.gro -r conf38.gro -p insane.top -n index.ndx -o npt38.tpr -maxwarn 10
gmx mdrun -deffnm npt38 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt38.gro -r npt38.gro -t npt38.cpt -p insane.top -n index.ndx -o umbrella38.tpr -maxwarn 10
gmx mdrun -deffnm umbrella38 -nb gpu -v 
