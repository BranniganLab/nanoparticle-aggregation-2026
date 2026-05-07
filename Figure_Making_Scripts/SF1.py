#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 15:45:53 2025

@author: jje63
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import Path
import argparse
from MDAnalysis.auxiliary.XVG import XVGReader


############### Draw Grid ##############

fig,ax = plt.subplots(2,3, figsize=(15,12), layout='constrained', sharex=True, sharey=True)
mpl.rcParams['xtick.labelsize'] = 25
mpl.rcParams['ytick.labelsize'] = 25

############# Making plottable Cluster Data #############
basepath = Path("../Simulation/Multi_Nanoparticle/Dimer_Free_Energy_System")
histo1 = basepath.joinpath("Polar/GNP_US/histo.xvg")
histo2 = basepath.joinpath("Polar/GNP_US_2/GNP_US/histo.xvg")
histo3 = basepath.joinpath("Polar/GNP_US_3/GNP_US/histo.xvg")

histo4 = basepath.joinpath("Hydrophobic/GNP_US_hyd/histo.xvg")
histo5 = basepath.joinpath("Hydrophobic/GNP_US_hyd_2/GNP_US_hyd/histo.xvg")
histo6 = basepath.joinpath("Hydrophobic/GNP_US_hyd_3/GNP_US_hyd/histo.xvg")

            
############# Plot on Grid #############
my_font = {'family': 'serif',
           'color':  'black',
           'weight': 'normal',
           'size': 20}
LWidth = 1
LStyle = 'solid'
MSize = 5
CSize = 4 
Ligand_Lengths = [8,12,16,20,24]
hydrophobic_color = "#003dfc"
polar_color = "#fc8900"
softsphere_color = "grey"

##### Make Data ################

Polar1 = XVGReader(histo1)
Polar2 = XVGReader(histo2)
Polar3 = XVGReader(histo3)

polart1 = []
polardata1 = []
for i in range(len(Polar1)):
    polart1.append(Polar1[i].time)
    polardata1.append(Polar1[i].data)

polart2 = []
polardata2 = []
for i in range(len(Polar2)):
    polart2.append(Polar2[i].time)
    polardata2.append(Polar2[i].data)

polart3 = []
polardata3 = []    
for i in range(len(Polar3)):
    polart3.append(Polar3[i].time)
    polardata3.append(Polar3[i].data)

Hydrophobic1 = XVGReader(histo4)
Hydrophobic2 = XVGReader(histo5)
Hydrophobic3 = XVGReader(histo6)

hydrophobict1 = []
hydrophobicdata1 = []
for i in range(len(Hydrophobic1)):
    hydrophobict1.append(Hydrophobic1[i].time)
    hydrophobicdata1.append(Hydrophobic1[i].data)

hydrophobict2 = []
hydrophobicdata2 = []
for i in range(len(Hydrophobic2)):
    hydrophobict2.append(Hydrophobic2[i].time)
    hydrophobicdata2.append(Hydrophobic2[i].data)

hydrophobict3 = []
hydrophobicdata3 = []    
for i in range(len(Hydrophobic3)):
    hydrophobict3.append(Hydrophobic3[i].time)
    hydrophobicdata3.append(Hydrophobic3[i].data)

################ Plot #############
fs = 20
fs2 = 15

ax[0,0].plot(polart1,polardata1)
ax[0,0].set_title("Polar Replica 1", fontsize=fs, loc='left')
ax[0,1].plot(polart2,polardata2)
ax[0,1].set_title("Polar Replica 2", fontsize=fs, loc='left')
ax[0,2].plot(polart3,polardata3)
ax[0,2].set_title("Polar Replica 3", fontsize=fs, loc='left')

ax[1,0].plot(hydrophobict1,hydrophobicdata1)
ax[1,0].set_title("Hydrophobic Replica 1", fontsize=fs, loc='left')
ax[1,1].plot(hydrophobict2,hydrophobicdata2)
ax[1,1].set_title("Hydrophobic Replica 2", fontsize=fs, loc='left')
ax[1,2].plot(hydrophobict3,hydrophobicdata3)
ax[1,2].set_title("Hydrophobic Replica 3", fontsize=fs, loc='left')

fig.supylabel('Counts', fontsize=30)
fig.supxlabel('Distance (nm)', fontsize=30)

fig.savefig(Path("../Graphs/SupplementaryFigure1.pdf"),format='pdf',dpi=500, bbox_inches='tight')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-sp","--showplot", help="Show the plot", action='store_true')
    args = parser.parse_args()
    if args.showplot:
        plt.show()  
