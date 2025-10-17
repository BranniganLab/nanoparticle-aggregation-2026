#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf628.gro -r conf628.gro -p insane.top -n index.ndx -o npt628.tpr -maxwarn 10
gmx mdrun -deffnm npt628 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt628.gro -r npt628.gro -t npt628.cpt -p insane.top -n index.ndx -o umbrella628.tpr -maxwarn 10
gmx mdrun -deffnm umbrella628 -nb gpu -v 
