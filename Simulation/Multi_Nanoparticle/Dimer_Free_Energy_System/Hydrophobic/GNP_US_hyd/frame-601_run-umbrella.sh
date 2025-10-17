#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf601.gro -r conf601.gro -p insane.top -n index.ndx -o npt601.tpr -maxwarn 10
gmx mdrun -deffnm npt601 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt601.gro -r npt601.gro -t npt601.cpt -p insane.top -n index.ndx -o umbrella601.tpr -maxwarn 10
gmx mdrun -deffnm umbrella601 -nb gpu -v 
