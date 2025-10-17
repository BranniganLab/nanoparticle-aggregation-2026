#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf346.gro -r conf346.gro -p insane.top -n index.ndx -o npt346.tpr -maxwarn 10
gmx mdrun -deffnm npt346 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt346.gro -r npt346.gro -t npt346.cpt -p insane.top -n index.ndx -o umbrella346.tpr -maxwarn 10
gmx mdrun -deffnm umbrella346 -nb gpu -v 
