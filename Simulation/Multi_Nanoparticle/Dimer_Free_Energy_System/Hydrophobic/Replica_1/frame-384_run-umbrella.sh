#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf384.gro -r conf384.gro -p insane.top -n index.ndx -o npt384.tpr -maxwarn 10
gmx mdrun -deffnm npt384 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt384.gro -r npt384.gro -t npt384.cpt -p insane.top -n index.ndx -o umbrella384.tpr -maxwarn 10
gmx mdrun -deffnm umbrella384 -nb gpu -v 
