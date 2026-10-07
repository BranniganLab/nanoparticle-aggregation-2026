#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf626.gro -r conf626.gro -p insane.top -n index.ndx -o npt626.tpr -maxwarn 10
gmx mdrun -deffnm npt626 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt626.gro -r npt626.gro -t npt626.cpt -p insane.top -n index.ndx -o umbrella626.tpr -maxwarn 10
gmx mdrun -deffnm umbrella626 -nb gpu -v 
