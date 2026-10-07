#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf388.gro -r conf388.gro -p insane.top -n index.ndx -o npt388.tpr -maxwarn 10
gmx mdrun -deffnm npt388 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt388.gro -r npt388.gro -t npt388.cpt -p insane.top -n index.ndx -o umbrella388.tpr -maxwarn 10
gmx mdrun -deffnm umbrella388 -nb gpu -v 
