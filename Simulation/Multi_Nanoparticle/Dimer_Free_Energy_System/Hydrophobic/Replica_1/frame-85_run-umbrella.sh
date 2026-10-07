#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf85.gro -r conf85.gro -p insane.top -n index.ndx -o npt85.tpr -maxwarn 10
gmx mdrun -deffnm npt85 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt85.gro -r npt85.gro -t npt85.cpt -p insane.top -n index.ndx -o umbrella85.tpr -maxwarn 10
gmx mdrun -deffnm umbrella85 -nb gpu -v 
