#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf176.gro -r conf176.gro -p insane.top -n index.ndx -o npt176.tpr -maxwarn 10
gmx mdrun -deffnm npt176 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt176.gro -r npt176.gro -t npt176.cpt -p insane.top -n index.ndx -o umbrella176.tpr -maxwarn 10
gmx mdrun -deffnm umbrella176 -nb gpu -v 
