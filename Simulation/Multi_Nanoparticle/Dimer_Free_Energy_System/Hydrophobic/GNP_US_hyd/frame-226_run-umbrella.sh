#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf226.gro -r conf226.gro -p insane.top -n index.ndx -o npt226.tpr -maxwarn 10
gmx mdrun -deffnm npt226 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt226.gro -r npt226.gro -t npt226.cpt -p insane.top -n index.ndx -o umbrella226.tpr -maxwarn 10
gmx mdrun -deffnm umbrella226 -nb gpu -v 
