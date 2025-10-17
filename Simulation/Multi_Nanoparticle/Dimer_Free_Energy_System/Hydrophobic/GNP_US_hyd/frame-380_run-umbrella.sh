#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf380.gro -r conf380.gro -p insane.top -n index.ndx -o npt380.tpr -maxwarn 10
gmx mdrun -deffnm npt380 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt380.gro -r npt380.gro -t npt380.cpt -p insane.top -n index.ndx -o umbrella380.tpr -maxwarn 10
gmx mdrun -deffnm umbrella380 -nb gpu -v 
