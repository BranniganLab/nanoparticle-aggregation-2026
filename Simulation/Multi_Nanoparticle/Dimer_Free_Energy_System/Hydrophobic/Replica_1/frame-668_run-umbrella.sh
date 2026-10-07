#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf668.gro -r conf668.gro -p insane.top -n index.ndx -o npt668.tpr -maxwarn 10
gmx mdrun -deffnm npt668 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt668.gro -r npt668.gro -t npt668.cpt -p insane.top -n index.ndx -o umbrella668.tpr -maxwarn 10
gmx mdrun -deffnm umbrella668 -nb gpu -v 
