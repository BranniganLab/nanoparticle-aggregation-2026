#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf42.gro -r conf42.gro -p insane.top -n index.ndx -o npt42.tpr -maxwarn 10
gmx mdrun -deffnm npt42 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt42.gro -r npt42.gro -t npt42.cpt -p insane.top -n index.ndx -o umbrella42.tpr -maxwarn 10
gmx mdrun -deffnm umbrella42 -nb gpu -v 
