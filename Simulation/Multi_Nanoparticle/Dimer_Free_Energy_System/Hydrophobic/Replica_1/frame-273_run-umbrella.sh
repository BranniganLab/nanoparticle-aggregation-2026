#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf273.gro -r conf273.gro -p insane.top -n index.ndx -o npt273.tpr -maxwarn 10
gmx mdrun -deffnm npt273 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt273.gro -r npt273.gro -t npt273.cpt -p insane.top -n index.ndx -o umbrella273.tpr -maxwarn 10
gmx mdrun -deffnm umbrella273 -nb gpu -v 
