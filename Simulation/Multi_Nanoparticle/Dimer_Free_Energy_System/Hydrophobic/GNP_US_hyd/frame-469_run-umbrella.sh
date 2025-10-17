#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf469.gro -r conf469.gro -p insane.top -n index.ndx -o npt469.tpr -maxwarn 10
gmx mdrun -deffnm npt469 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt469.gro -r npt469.gro -t npt469.cpt -p insane.top -n index.ndx -o umbrella469.tpr -maxwarn 10
gmx mdrun -deffnm umbrella469 -nb gpu -v 
