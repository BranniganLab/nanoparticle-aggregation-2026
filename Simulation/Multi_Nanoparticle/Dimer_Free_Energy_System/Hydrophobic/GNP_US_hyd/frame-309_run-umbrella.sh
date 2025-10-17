#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf309.gro -r conf309.gro -p insane.top -n index.ndx -o npt309.tpr -maxwarn 10
gmx mdrun -deffnm npt309 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt309.gro -r npt309.gro -t npt309.cpt -p insane.top -n index.ndx -o umbrella309.tpr -maxwarn 10
gmx mdrun -deffnm umbrella309 -nb gpu -v 
