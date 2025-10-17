#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf201.gro -r conf201.gro -p insane.top -n index.ndx -o npt201.tpr -maxwarn 10
gmx mdrun -deffnm npt201 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt201.gro -r npt201.gro -t npt201.cpt -p insane.top -n index.ndx -o umbrella201.tpr -maxwarn 10
gmx mdrun -deffnm umbrella201 -nb gpu -v 
