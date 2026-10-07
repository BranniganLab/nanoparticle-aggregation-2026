#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf658.gro -r conf658.gro -p insane.top -n index.ndx -o npt658.tpr -maxwarn 10
gmx mdrun -deffnm npt658 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt658.gro -r npt658.gro -t npt658.cpt -p insane.top -n index.ndx -o umbrella658.tpr -maxwarn 10
gmx mdrun -deffnm umbrella658 -nb gpu -v 
