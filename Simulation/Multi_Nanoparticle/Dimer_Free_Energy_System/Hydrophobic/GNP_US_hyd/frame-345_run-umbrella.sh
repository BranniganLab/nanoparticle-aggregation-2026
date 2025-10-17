#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf345.gro -r conf345.gro -p insane.top -n index.ndx -o npt345.tpr -maxwarn 10
gmx mdrun -deffnm npt345 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt345.gro -r npt345.gro -t npt345.cpt -p insane.top -n index.ndx -o umbrella345.tpr -maxwarn 10
gmx mdrun -deffnm umbrella345 -nb gpu -v 
