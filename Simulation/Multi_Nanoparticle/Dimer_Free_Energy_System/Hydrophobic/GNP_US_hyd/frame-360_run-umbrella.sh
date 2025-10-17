#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf360.gro -r conf360.gro -p insane.top -n index.ndx -o npt360.tpr -maxwarn 10
gmx mdrun -deffnm npt360 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt360.gro -r npt360.gro -t npt360.cpt -p insane.top -n index.ndx -o umbrella360.tpr -maxwarn 10
gmx mdrun -deffnm umbrella360 -nb gpu -v 
