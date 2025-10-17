#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf280.gro -r conf280.gro -p insane.top -n index.ndx -o npt280.tpr -maxwarn 10
gmx mdrun -deffnm npt280 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt280.gro -r npt280.gro -t npt280.cpt -p insane.top -n index.ndx -o umbrella280.tpr -maxwarn 10
gmx mdrun -deffnm umbrella280 -nb gpu -v 
