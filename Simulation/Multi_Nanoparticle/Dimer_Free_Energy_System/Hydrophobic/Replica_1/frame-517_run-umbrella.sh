#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf517.gro -r conf517.gro -p insane.top -n index.ndx -o npt517.tpr -maxwarn 10
gmx mdrun -deffnm npt517 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt517.gro -r npt517.gro -t npt517.cpt -p insane.top -n index.ndx -o umbrella517.tpr -maxwarn 10
gmx mdrun -deffnm umbrella517 -nb gpu -v 
