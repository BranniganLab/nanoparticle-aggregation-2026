#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf418.gro -r conf418.gro -p insane.top -n index.ndx -o npt418.tpr -maxwarn 10
gmx mdrun -deffnm npt418 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt418.gro -r npt418.gro -t npt418.cpt -p insane.top -n index.ndx -o umbrella418.tpr -maxwarn 10
gmx mdrun -deffnm umbrella418 -nb gpu -v 
