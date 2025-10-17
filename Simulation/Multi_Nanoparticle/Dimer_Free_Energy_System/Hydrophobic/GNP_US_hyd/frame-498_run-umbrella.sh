#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf498.gro -r conf498.gro -p insane.top -n index.ndx -o npt498.tpr -maxwarn 10
gmx mdrun -deffnm npt498 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt498.gro -r npt498.gro -t npt498.cpt -p insane.top -n index.ndx -o umbrella498.tpr -maxwarn 10
gmx mdrun -deffnm umbrella498 -nb gpu -v 
