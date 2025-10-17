#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf329.gro -r conf329.gro -p insane.top -n index.ndx -o npt329.tpr -maxwarn 10
gmx mdrun -deffnm npt329 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt329.gro -r npt329.gro -t npt329.cpt -p insane.top -n index.ndx -o umbrella329.tpr -maxwarn 10
gmx mdrun -deffnm umbrella329 -nb gpu -v 
