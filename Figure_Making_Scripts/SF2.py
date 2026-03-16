#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 13:42:41 2026

@author: jje63
"""
import sys
import matplotlib.pyplot as plt
from pathlib import Path
from MDAnalysis.auxiliary.XVG import XVGReader
import numpy as np
import pandas as pd
import argparse
from matplotlib.lines import Line2D
sys.path.insert(0, "../Analysis/Figure_3_scripts/")
from ClusterPlotter import generalCluster, multiClusterData 


############### Draw Grid ##############

fig,ax = plt.subplots(3,5, figsize=(15,10), layout='constrained', sharex=True, sharey=True)
fig1,ax1 = plt.subplots(3,5, figsize=(15,10), layout='constrained', sharex=True, sharey=True)

############# Making plottable Cluster Data #############
basepath = Path("../Simulation/Multi_Nanoparticle/10_NP_Systems")
sub_dir_base = ["Hydrophobic","Polar","Soft_Sphere" ]
thiol_name = ["Octanethiol", "Dodecanethiol","Hexadecanethiol","Icosanethiol","Tetracosanethiol"]
file_name = "analysis/fullclusterAU10.dat"
data_bins_la = [pd.DataFrame(),pd.DataFrame(),pd.DataFrame()]
data_bins_mf = [pd.DataFrame(),pd.DataFrame(),pd.DataFrame()]
scaling_factor = 100

for i, sub_d in enumerate(sub_dir_base):
        bins_la = data_bins_la[i]
        bins_mf = data_bins_mf[i]
        for j in range(len(thiol_name)):
            paths = basepath.glob(sub_dir_base[i]+"*/"+thiol_name[j]+"/Replica_[1-5]/"+file_name)
            #data = multiClusterData(paths)
            #bins[thiol_name[j]] = {}
            for k, path in enumerate(paths):
                data = generalCluster(path)
                bins_la[thiol_name[j]+"_"+str(k)] = data.largest_aggregate_fraction_over_time
                bins_mf[thiol_name[j]+"_"+str(k)] = data.monomer_fraction_over_time

data_bins_la[0].index = data_bins_la[0].index / scaling_factor
data_bins_la[1].index = data_bins_la[1].index / scaling_factor
data_bins_la[2].index = data_bins_la[2].index / scaling_factor

data_bins_mf[0].index = data_bins_mf[0].index / scaling_factor
data_bins_mf[1].index = data_bins_mf[1].index / scaling_factor
data_bins_mf[2].index = data_bins_mf[2].index / scaling_factor
############# Plot on Grid #############
my_font = {'family': 'serif',
           'color':  'black',
           'weight': 'normal',
           'size': 10}
LWidth = 2
LStyle = 'solid'
MSize = 5
CSize = 4 


################ Plot #############

## LAF ##
for i in range(len(sub_dir_base)):
    for k in range(5):
        if i == 0:
            TT = "Replica "+str(k+1)
        else:
            TT =""
        if k == 0:
            plt.setp(ax[i,k], ylabel=sub_dir_base[i].replace("_"," "))
        else:
            y_axis = ""
        cols_to_plot = data_bins_la[i].columns[data_bins_la[i].columns.str.contains(str(k))]
        Rep1_subset = data_bins_la[i][cols_to_plot]
        Rep1_subset.plot(ax=ax[i,k],
                         kind="line",
                         title=TT,
                         legend=False,
                         linewidth = LWidth
                         #ylabel=y_axis
                         )
fig.supylabel('Largest aggregate fraction', fontsize=14)
fig.supxlabel(r'Time ($\mu s$)', fontsize=14)

color_list = [line.get_color() for line in ax[0,0].lines]
legend_list = []
for color in color_list:
    legend_list.append(Line2D([0], [0], color=color, lw=4))
fig.legend(legend_list, thiol_name, ncol=len(thiol_name), loc="upper center",bbox_to_anchor=(0.5, 1.05))


## MF ##
for i in range(len(sub_dir_base)):
    for k in range(5):
        if i == 0:
            TT = "Replica "+str(k+1)
        else:
            TT =""
        if k == 0:
            plt.setp(ax1[i,k], ylabel=sub_dir_base[i].replace("_"," "))
        else:
            y_axis = ""
        cols_to_plot = data_bins_mf[i].columns[data_bins_mf[i].columns.str.contains(str(k))]
        Rep1_subset = data_bins_mf[i][cols_to_plot]
        Rep1_subset.plot(ax=ax1[i,k],
                         kind="line",
                         title=TT,
                         legend=False,
                         linewidth = LWidth
                         #ylabel=y_axis
                         )
fig1.supylabel('Monomer fraction', fontsize=14)
fig1.supxlabel(r'Time ($\mu s$)', fontsize=14)

color_list = [line.get_color() for line in ax[0,0].lines]
legend_list = []
for color in color_list:
    legend_list.append(Line2D([0], [0], color=color, lw=4))
fig1.legend(legend_list, thiol_name, ncol=len(thiol_name), loc="upper center",bbox_to_anchor=(0.5, 1.05))

fig.savefig(Path("../Graphs/SupplementaryFigure2_1.pdf"),format='pdf',dpi=500, bbox_inches='tight')
fig1.savefig(Path("../Graphs/SupplementaryFigure2_2.pdf"),format='pdf',dpi=500, bbox_inches='tight')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-sp","--showplot", help="Show the plot", action='store_true')
    args = parser.parse_args()
    if args.showplot:
        plt.show()  
