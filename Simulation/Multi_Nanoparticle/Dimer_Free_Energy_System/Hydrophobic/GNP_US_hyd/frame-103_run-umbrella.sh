#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf103.gro -r conf103.gro -p insane.top -n index.ndx -o npt103.tpr -maxwarn 10
gmx mdrun -deffnm npt103 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt103.gro -r npt103.gro -t npt103.cpt -p insane.top -n index.ndx -o umbrella103.tpr -maxwarn 10
gmx mdrun -deffnm umbrella103 -nb gpu -v 
