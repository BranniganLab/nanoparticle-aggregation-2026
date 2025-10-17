#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf466.gro -r conf466.gro -p insane.top -n index.ndx -o npt466.tpr -maxwarn 10
gmx mdrun -deffnm npt466 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt466.gro -r npt466.gro -t npt466.cpt -p insane.top -n index.ndx -o umbrella466.tpr -maxwarn 10
gmx mdrun -deffnm umbrella466 -nb gpu -v 
