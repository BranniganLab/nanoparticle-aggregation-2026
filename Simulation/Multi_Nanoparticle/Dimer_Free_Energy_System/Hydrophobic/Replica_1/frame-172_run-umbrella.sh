#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf172.gro -r conf172.gro -p insane.top -n index.ndx -o npt172.tpr -maxwarn 10
gmx mdrun -deffnm npt172 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt172.gro -r npt172.gro -t npt172.cpt -p insane.top -n index.ndx -o umbrella172.tpr -maxwarn 10
gmx mdrun -deffnm umbrella172 -nb gpu -v 
