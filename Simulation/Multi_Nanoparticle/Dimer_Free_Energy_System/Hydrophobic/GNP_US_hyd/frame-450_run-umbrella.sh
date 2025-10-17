#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf450.gro -r conf450.gro -p insane.top -n index.ndx -o npt450.tpr -maxwarn 10
gmx mdrun -deffnm npt450 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt450.gro -r npt450.gro -t npt450.cpt -p insane.top -n index.ndx -o umbrella450.tpr -maxwarn 10
gmx mdrun -deffnm umbrella450 -nb gpu -v 
