#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf21.gro -r conf21.gro -p insane.top -n index.ndx -o npt21.tpr -maxwarn 10
gmx mdrun -deffnm npt21 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt21.gro -r npt21.gro -t npt21.cpt -p insane.top -n index.ndx -o umbrella21.tpr -maxwarn 10
gmx mdrun -deffnm umbrella21 -nb gpu -v 
