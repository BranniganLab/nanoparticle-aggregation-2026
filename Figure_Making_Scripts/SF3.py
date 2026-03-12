#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 13:42:41 2026

@author: jje63
"""
import sys
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
from matplotlib.lines import Line2D
sys.path.insert(0, "../Analysis/Figure_1_scripts/")
from SASAplotter import generalSASA, make_thiol_dataset, create_sasa_core_replica_data, create_sasa_full_replica_data
from order_density_contact_potter import generalFileParse, create_contact_core_replica_data, create_contact_full_replica_data,make_thiol_dataset_O_C


############### Draw Grid ##############

fig,ax = plt.subplots(6,3, figsize=(15,10), sharey=True)
fig1,ax1 = plt.subplots(6,3, figsize=(15,10), layout='constrained', sharey=True)

############# Making plottable Cluster Data #############
DIRECTORY_PATH = Path("../Simulation/Single_Nanoparticle")
CORETYPES = ["C1","C5","N0","P1","P5"]
CORETYPES2 = ["C1","C5","N0","P1","P5","SS"]
THIOL = ["Octanethiol","Dodecanethiol","Hexadecanethiol","Icosanethiol","Tetracosanethiol"]
#REPLICA = ["Replica1","Replica2","Replica3"]
LENGTHS = [2,3,4,5,6]
DATA_FILE="watersasa"+".dat"

C1data = make_thiol_dataset(DIRECTORY_PATH, "C1", "*thiol", "Replica*",DATA_FILE, cutoff=0)
C5data = make_thiol_dataset(DIRECTORY_PATH, "C5", "*thiol", "Replica*",DATA_FILE, cutoff=0)
N0data = make_thiol_dataset(DIRECTORY_PATH, "N0", "*thiol", "Replica*",DATA_FILE, cutoff=0)
P1data = make_thiol_dataset(DIRECTORY_PATH, "P1", "*thiol", "Replica*",DATA_FILE, cutoff=0)
P5data = make_thiol_dataset(DIRECTORY_PATH, "P5", "*thiol", "Replica*",DATA_FILE, cutoff=0)
SSdata = make_thiol_dataset(DIRECTORY_PATH, "SS", "*thiol", "Replica*",DATA_FILE, cutoff=0)
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
def combine_replicas(thiol_dataset):
    Replica1 = pd.DataFrame()
    Replica2 = pd.DataFrame()
    Replica3 = pd.DataFrame()
    for key,val in thiol_dataset.items():
        name = key.split("_")
        if name[1] == "Replica1":
            Replica1[name[0]] = val.sasa_data_frame["Values"]
        if name[1] == "Replica2":
            Replica2[name[0]] = val.sasa_data_frame["Values"]
        if name[1] == "Replica3":
            Replica3[name[0]] = val.sasa_data_frame["Values"]

    return (Replica1, Replica2, Replica3)

def plot_reps(combined_reps, axes, row, xname):
    for i,data in enumerate(combined_reps):
        data.plot(ax=axes[row, i],
                  legend=False)
    plt.setp(ax[row,0], ylabel=CORETYPES2[row])

ax[0,0].set_xlabel("C1")
plot_reps(combine_replicas(C1data), ax, 0, "C1")
plot_reps(combine_replicas(C5data), ax, 1, "C5")
plot_reps(combine_replicas(N0data), ax, 2, "N0")
plot_reps(combine_replicas(P1data), ax, 3, "P1")
plot_reps(combine_replicas(P5data), ax, 4, "P5")
plot_reps(combine_replicas(SSdata), ax, 5, "SS")

color_list = [line.get_color() for line in ax[0,0].lines]
legend_list = []
for color in color_list:
    legend_list.append(Line2D([0], [0], color=color, lw=4))
fig.legend(legend_list, THIOL, ncol=len(THIOL), loc="upper center",bbox_to_anchor=(0.5, 1.05))

plt.show()