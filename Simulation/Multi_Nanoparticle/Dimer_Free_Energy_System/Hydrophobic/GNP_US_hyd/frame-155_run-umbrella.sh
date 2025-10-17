#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf155.gro -r conf155.gro -p insane.top -n index.ndx -o npt155.tpr -maxwarn 10
gmx mdrun -deffnm npt155 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt155.gro -r npt155.gro -t npt155.cpt -p insane.top -n index.ndx -o umbrella155.tpr -maxwarn 10
gmx mdrun -deffnm umbrella155 -nb gpu -v 
