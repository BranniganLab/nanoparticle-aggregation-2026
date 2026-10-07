#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf594.gro -r conf594.gro -p insane.top -n index.ndx -o npt594.tpr -maxwarn 10
gmx mdrun -deffnm npt594 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt594.gro -r npt594.gro -t npt594.cpt -p insane.top -n index.ndx -o umbrella594.tpr -maxwarn 10
gmx mdrun -deffnm umbrella594 -nb gpu -v 
