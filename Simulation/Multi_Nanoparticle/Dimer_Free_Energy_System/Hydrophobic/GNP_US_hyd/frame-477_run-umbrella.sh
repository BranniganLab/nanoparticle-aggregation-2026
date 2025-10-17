#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf477.gro -r conf477.gro -p insane.top -n index.ndx -o npt477.tpr -maxwarn 10
gmx mdrun -deffnm npt477 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt477.gro -r npt477.gro -t npt477.cpt -p insane.top -n index.ndx -o umbrella477.tpr -maxwarn 10
gmx mdrun -deffnm umbrella477 -nb gpu -v 
