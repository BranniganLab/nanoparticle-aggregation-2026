#!/bin/bash

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c conf614.gro -r conf614.gro -p insane.top -n index.ndx -o npt614.tpr -maxwarn 10
gmx mdrun -deffnm npt614 -nb gpu -v

# Umbrella run
gmx grompp -f md_umbrella.mdp -c npt614.gro -r npt614.gro -t npt614.cpt -p insane.top -n index.ndx -o umbrella614.tpr -maxwarn 10
gmx mdrun -deffnm umbrella614 -nb gpu -v 
