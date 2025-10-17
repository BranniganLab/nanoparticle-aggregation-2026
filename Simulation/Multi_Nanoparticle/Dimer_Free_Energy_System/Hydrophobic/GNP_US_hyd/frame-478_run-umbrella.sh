#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf478.gro -r conf478.gro -p insane.top -n index.ndx -o npt478.tpr -maxwarn 10
gmx mdrun -deffnm npt478 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt478.gro -r npt478.gro -t npt478.cpt -p insane.top -n index.ndx -o umbrella478.tpr -maxwarn 10
gmx mdrun -deffnm umbrella478 -nb gpu -v 
