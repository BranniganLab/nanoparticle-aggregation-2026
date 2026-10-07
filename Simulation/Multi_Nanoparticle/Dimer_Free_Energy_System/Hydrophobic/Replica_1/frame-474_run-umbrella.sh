#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf474.gro -r conf474.gro -p insane.top -n index.ndx -o npt474.tpr -maxwarn 10
gmx mdrun -deffnm npt474 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt474.gro -r npt474.gro -t npt474.cpt -p insane.top -n index.ndx -o umbrella474.tpr -maxwarn 10
gmx mdrun -deffnm umbrella474 -nb gpu -v 
