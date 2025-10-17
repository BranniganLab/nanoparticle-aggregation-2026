#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf595.gro -r conf595.gro -p insane.top -n index.ndx -o npt595.tpr -maxwarn 10
gmx mdrun -deffnm npt595 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt595.gro -r npt595.gro -t npt595.cpt -p insane.top -n index.ndx -o umbrella595.tpr -maxwarn 10
gmx mdrun -deffnm umbrella595 -nb gpu -v 
