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

D1 = 10
D2 = 5
fig_la_oct,ax_la_oct = plt.subplots(1,3, figsize=(D1,D2), layout='constrained', sharex=True, sharey=True)
fig_la_dod,ax_la_dod = plt.subplots(1,3, figsize=(D1,D2), layout='constrained', sharex=True, sharey=True)
fig_la_hex,ax_la_hex = plt.subplots(1,3, figsize=(D1,D2), layout='constrained', sharex=True, sharey=True)
fig_la_ico,ax_la_ico = plt.subplots(1,3, figsize=(D1,D2), layout='constrained', sharex=True, sharey=True)
fig_la_tet,ax_la_tet = plt.subplots(1,3, figsize=(D1,D2), layout='constrained', sharex=True, sharey=True)

la_plots = [fig_la_oct, fig_la_dod, fig_la_hex, fig_la_ico, fig_la_tet]
la_axes = [ax_la_oct, ax_la_dod, ax_la_hex, ax_la_ico, ax_la_tet]

fig_mf_oct,ax_mf_oct = plt.subplots(1,3, figsize=(D1,D2), layout='constrained', sharex=True, sharey=True)
fig_mf_dod,ax_mf_dod = plt.subplots(1,3, figsize=(D1,D2), layout='constrained', sharex=True, sharey=True)
fig_mf_hex,ax_mf_hex = plt.subplots(1,3, figsize=(D1,D2), layout='constrained', sharex=True, sharey=True)
fig_mf_ico,ax_mf_ico = plt.subplots(1,3, figsize=(D1,D2), layout='constrained', sharex=True, sharey=True)
fig_mf_tet,ax_mf_tet = plt.subplots(1,3, figsize=(D1,D2), layout='constrained', sharex=True, sharey=True)

mf_plots = [fig_mf_oct, fig_mf_dod, fig_mf_hex, fig_mf_ico, fig_mf_tet]
mf_axes = [ax_mf_oct, ax_mf_dod, ax_mf_hex, ax_mf_ico, ax_mf_tet]

############# Making plottable Cluster Data #############
basepath = Path("../Simulation/Multi_Nanoparticle/10_NP_Systems")
sub_dir_base = ["Hydrophobic","Polar","Soft_Sphere" ]
thiol_name = ["Octanethiol", "Dodecanethiol","Hexadecanethiol","Icosanethiol","Tetracosanethiol"]
replica_name = ["Replica 1", "Replica 2", "Replica 3", "Replica 4", "Replica 5"]
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
fs = 20

################ Plot #############

## LAF ##
for i in range(len(sub_dir_base)):
    for j,thiol in enumerate(thiol_name):
        cols_to_plot = data_bins_la[i].columns[data_bins_la[i].columns.str.contains(thiol)]
        Thiol_subset = data_bins_la[i][cols_to_plot]
        Thiol_subset.plot(ax=la_axes[j][i],
                         kind="line",
                         title=sub_dir_base[i],
                         legend=False,
                         linewidth = LWidth,
                         fontsize = 15
                         )
        la_axes[j][i].set_title(sub_dir_base[i], fontsize=15)
        la_plots[j].supylabel('Largest aggregate fraction', fontsize=fs)
        la_plots[j].supxlabel(r'Time ($\mu s$)', fontsize=fs)

        color_list = [line.get_color() for line in la_axes[j][i].lines]
        legend_list = []
        for color in color_list:
            legend_list.append(Line2D([0], [0], color=color, lw=4))
        la_plots[j].legend(legend_list, replica_name, ncol=len(replica_name), loc="upper center",bbox_to_anchor=(0.5, 1.12), fontsize=15)
        
        la_plots[j].savefig(Path(f"../Graphs/SupplementaryFigure2_la_{thiol}.pdf"),format='pdf',dpi=500, bbox_inches='tight')

## MF ##
for i in range(len(sub_dir_base)):
    for j,thiol in enumerate(thiol_name):
        cols_to_plot = data_bins_mf[i].columns[data_bins_la[i].columns.str.contains(thiol)]
        Thiol_subset = data_bins_mf[i][cols_to_plot]
        Thiol_subset.plot(ax=mf_axes[j][i],
                         kind="line",
                         #title=sub_dir_base[i],
                         legend=False,
                         linewidth = LWidth,
                         fontsize = 15
                         )
        mf_axes[j][i].set_title(sub_dir_base[i], fontsize=15)
        mf_plots[j].supylabel('Largest aggregate fraction', fontsize=fs)
        mf_plots[j].supxlabel(r'Time ($\mu s$)', fontsize=fs)

        color_list = [line.get_color() for line in mf_axes[j][i].lines]
        legend_list = []
        for color in color_list:
            legend_list.append(Line2D([0], [0], color=color, lw=4))
        mf_plots[j].legend(legend_list, replica_name, ncol=len(replica_name), loc="upper center",bbox_to_anchor=(0.5, 1.12), fontsize=15)
        mf_plots[j].savefig(Path(f"../Graphs/SupplementaryFigure2_mf_{thiol}.pdf"),format='pdf',dpi=500, bbox_inches='tight')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-sp","--showplot", help="Show the plot", action='store_true')
    args = parser.parse_args()
    if args.showplot:
        plt.show()
