#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf300.gro -r conf300.gro -p insane.top -n index.ndx -o npt300.tpr -maxwarn 10
gmx mdrun -deffnm npt300 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt300.gro -r npt300.gro -t npt300.cpt -p insane.top -n index.ndx -o umbrella300.tpr -maxwarn 10
gmx mdrun -deffnm umbrella300 -nb gpu -v 
