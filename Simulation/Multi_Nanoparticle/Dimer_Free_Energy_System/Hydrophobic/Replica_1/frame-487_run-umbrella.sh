#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf487.gro -r conf487.gro -p insane.top -n index.ndx -o npt487.tpr -maxwarn 10
gmx mdrun -deffnm npt487 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt487.gro -r npt487.gro -t npt487.cpt -p insane.top -n index.ndx -o umbrella487.tpr -maxwarn 10
gmx mdrun -deffnm umbrella487 -nb gpu -v 
