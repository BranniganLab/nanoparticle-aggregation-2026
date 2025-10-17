#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf153.gro -r conf153.gro -p insane.top -n index.ndx -o npt153.tpr -maxwarn 10
gmx mdrun -deffnm npt153 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt153.gro -r npt153.gro -t npt153.cpt -p insane.top -n index.ndx -o umbrella153.tpr -maxwarn 10
gmx mdrun -deffnm umbrella153 -nb gpu -v 
