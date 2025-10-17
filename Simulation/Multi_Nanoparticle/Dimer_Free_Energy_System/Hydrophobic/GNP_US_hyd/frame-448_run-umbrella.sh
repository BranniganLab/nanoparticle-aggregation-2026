#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf448.gro -r conf448.gro -p insane.top -n index.ndx -o npt448.tpr -maxwarn 10
gmx mdrun -deffnm npt448 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt448.gro -r npt448.gro -t npt448.cpt -p insane.top -n index.ndx -o umbrella448.tpr -maxwarn 10
gmx mdrun -deffnm umbrella448 -nb gpu -v 
