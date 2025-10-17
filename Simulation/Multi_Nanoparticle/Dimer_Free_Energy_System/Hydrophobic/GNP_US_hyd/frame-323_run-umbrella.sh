#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf323.gro -r conf323.gro -p insane.top -n index.ndx -o npt323.tpr -maxwarn 10
gmx mdrun -deffnm npt323 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt323.gro -r npt323.gro -t npt323.cpt -p insane.top -n index.ndx -o umbrella323.tpr -maxwarn 10
gmx mdrun -deffnm umbrella323 -nb gpu -v 
