#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf607.gro -r conf607.gro -p insane.top -n index.ndx -o npt607.tpr -maxwarn 10
gmx mdrun -deffnm npt607 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt607.gro -r npt607.gro -t npt607.cpt -p insane.top -n index.ndx -o umbrella607.tpr -maxwarn 10
gmx mdrun -deffnm umbrella607 -nb gpu -v 
