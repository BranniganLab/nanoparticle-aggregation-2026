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

fig,ax = plt.subplots(6,3, figsize=(15,10), layout='constrained', sharex=True)
fig1,ax1 = plt.subplots(6,3, figsize=(15,10), layout='constrained', sharex=True)
fig2,ax2 = plt.subplots(6,3, figsize=(15,10), layout='constrained', sharex=True)
fig3,ax3 = plt.subplots(6,3, figsize=(15,10), layout='constrained', sharex=True)
############# Making plottable Cluster Data #############
DIRECTORY_PATH = Path("../Simulation/Single_Nanoparticle")
CORETYPES = ["C1","C5","N0","P1","P5"]
CORETYPES2 = ["C1","C5","N0","P1","P5","SS"]
THIOL = ["Octanethiol","Dodecanethiol","Hexadecanethiol","Icosanethiol","Tetracosanethiol"]
#REPLICA = ["Replica1","Replica2","Replica3"]
LENGTHS = [2,3,4,5,6]
DATA_FILE="watersasa"+".dat"

C1data_wat = make_thiol_dataset(DIRECTORY_PATH, "C1", "*thiol", "Replica*",DATA_FILE, cutoff=0)
C5data_wat = make_thiol_dataset(DIRECTORY_PATH, "C5", "*thiol", "Replica*",DATA_FILE, cutoff=0)
N0data_wat = make_thiol_dataset(DIRECTORY_PATH, "N0", "*thiol", "Replica*",DATA_FILE, cutoff=0)
P1data_wat = make_thiol_dataset(DIRECTORY_PATH, "P1", "*thiol", "Replica*",DATA_FILE, cutoff=0)
P5data_wat = make_thiol_dataset(DIRECTORY_PATH, "P5", "*thiol", "Replica*",DATA_FILE, cutoff=0)
SSdata_wat = make_thiol_dataset(DIRECTORY_PATH, "SS", "*thiol", "Replica*",DATA_FILE, cutoff=0)

DATA_FILE="lipidsasa"+".dat"

C1data_lip = make_thiol_dataset(DIRECTORY_PATH, "C1", "*thiol", "Replica*",DATA_FILE, cutoff=0)
C5data_lip = make_thiol_dataset(DIRECTORY_PATH, "C5", "*thiol", "Replica*",DATA_FILE, cutoff=0)
N0data_lip = make_thiol_dataset(DIRECTORY_PATH, "N0", "*thiol", "Replica*",DATA_FILE, cutoff=0)
P1data_lip = make_thiol_dataset(DIRECTORY_PATH, "P1", "*thiol", "Replica*",DATA_FILE, cutoff=0)
P5data_lip = make_thiol_dataset(DIRECTORY_PATH, "P5", "*thiol", "Replica*",DATA_FILE, cutoff=0)
SSdata_lip = make_thiol_dataset(DIRECTORY_PATH, "SS", "*thiol", "Replica*",DATA_FILE, cutoff=0)

DATA_FILE="headcont"+".dat"

C1data_head = make_thiol_dataset_O_C(DIRECTORY_PATH, "C1", "*thiol", "Replica*",DATA_FILE, "contact")
C5data_head = make_thiol_dataset_O_C(DIRECTORY_PATH, "C5", "*thiol", "Replica*",DATA_FILE, "contact")
N0data_head = make_thiol_dataset_O_C(DIRECTORY_PATH, "N0", "*thiol", "Replica*",DATA_FILE, "contact")
P1data_head = make_thiol_dataset_O_C(DIRECTORY_PATH, "P1", "*thiol", "Replica*",DATA_FILE, "contact")
P5data_head = make_thiol_dataset_O_C(DIRECTORY_PATH, "P5", "*thiol", "Replica*",DATA_FILE, "contact")
SSdata_head = make_thiol_dataset_O_C(DIRECTORY_PATH, "SS", "*thiol", "Replica*",DATA_FILE, "contact")

DATA_FILE="tailcont"+".dat"

C1data_tail = make_thiol_dataset_O_C(DIRECTORY_PATH, "C1", "*thiol", "Replica*",DATA_FILE, "contact")
C5data_tail = make_thiol_dataset_O_C(DIRECTORY_PATH, "C5", "*thiol", "Replica*",DATA_FILE, "contact")
N0data_tail = make_thiol_dataset_O_C(DIRECTORY_PATH, "N0", "*thiol", "Replica*",DATA_FILE, "contact")
P1data_tail = make_thiol_dataset_O_C(DIRECTORY_PATH, "P1", "*thiol", "Replica*",DATA_FILE, "contact")
P5data_tail = make_thiol_dataset_O_C(DIRECTORY_PATH, "P5", "*thiol", "Replica*",DATA_FILE, "contact")
SSdata_tail = make_thiol_dataset_O_C(DIRECTORY_PATH, "SS", "*thiol", "Replica*",DATA_FILE, "contact")
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
def combine_replicas(thiol_dataset, datatype="SASA"):
    Replica1 = pd.DataFrame()
    Replica2 = pd.DataFrame()
    Replica3 = pd.DataFrame()
    for key,val in thiol_dataset.items():
        name = key.split("_")
        if name[1] == "Replica1":
            if datatype == "SASA":
                Replica1[name[0]] = val.sasa_data_frame["Values"]
            else:
                Replica1[name[0]] = val.data_frame["Values"]
        if name[1] == "Replica2":
            if datatype == "SASA":
                Replica2[name[0]] = val.sasa_data_frame["Values"]
            else:
                Replica2[name[0]] = val.data_frame["Values"]
        if name[1] == "Replica3":
            if datatype == "SASA":
                Replica3[name[0]] = val.sasa_data_frame["Values"]
            else:
                Replica3[name[0]] = val.data_frame["Values"]

    return (Replica1, Replica2, Replica3)

def plot_reps(combined_reps, axes, row, xname):
    for i,data in enumerate(combined_reps):
        if len(data) != 1003:
            print(len(data), )
        if CORETYPES2[row] == "C1":
            TT = "Replica "+str(i+1)
        else:
            TT =""
        data["Time"] = np.arange(len(data))/100
        data.plot(ax=axes[row, i],
                  x="Time",
                  y=THIOL,
                  title=TT,
                  xlabel='',
                  legend=False)
    plt.setp(axes[row,0], ylabel=CORETYPES2[row])

plot_reps(combine_replicas(C1data_wat), ax, 0, "C1")
plot_reps(combine_replicas(C5data_wat), ax, 1, "C5")
plot_reps(combine_replicas(N0data_wat), ax, 2, "N0")
plot_reps(combine_replicas(P1data_wat), ax, 3, "P1")
plot_reps(combine_replicas(P5data_wat), ax, 4, "P5")
plot_reps(combine_replicas(SSdata_wat), ax, 5, "SS")

fig.supylabel(r'Water Accesible Surface Area($nm^{2}$)', fontsize=14)
fig.supxlabel(r'Time (ns)', fontsize=14)

plot_reps(combine_replicas(C1data_lip), ax1, 0, "C1")
plot_reps(combine_replicas(C5data_lip), ax1, 1, "C5")
plot_reps(combine_replicas(N0data_lip), ax1, 2, "N0")
plot_reps(combine_replicas(P1data_lip), ax1, 3, "P1")
plot_reps(combine_replicas(P5data_lip), ax1, 4, "P5")
plot_reps(combine_replicas(SSdata_lip), ax1, 5, "SS")

fig1.supylabel(r'Lipid Accesible Surface Area($nm^{2}$)', fontsize=14)
fig1.supxlabel(r'Time (ns)', fontsize=14)

DT = "contact"
plot_reps(combine_replicas(C1data_head, DT), ax2, 0, "C1")
plot_reps(combine_replicas(C5data_head, DT), ax2, 1, "C5")
plot_reps(combine_replicas(N0data_head, DT), ax2, 2, "N0")
plot_reps(combine_replicas(P1data_head, DT), ax2, 3, "P1")
plot_reps(combine_replicas(P5data_head, DT), ax2, 4, "P5")
plot_reps(combine_replicas(SSdata_head, DT), ax2, 5, "SS")

fig2.supylabel(r'Number of Lipid Head Contacts', fontsize=14)
fig2.supxlabel(r'Time (ns)', fontsize=14)

plot_reps(combine_replicas(C1data_tail, DT), ax3, 0, "C1")
plot_reps(combine_replicas(C5data_tail, DT), ax3, 1, "C5")
plot_reps(combine_replicas(N0data_tail, DT), ax3, 2, "N0")
plot_reps(combine_replicas(P1data_tail, DT), ax3, 3, "P1")
plot_reps(combine_replicas(P5data_tail, DT), ax3, 4, "P5")
plot_reps(combine_replicas(SSdata_tail, DT), ax3, 5, "SS")

fig3.supylabel(r'Number of Lipid Tail Contacts', fontsize=14)
fig3.supxlabel(r'Time (ns)', fontsize=14)

color_list = [line.get_color() for line in ax[0,0].lines]
legend_list = []
for color in color_list:
    legend_list.append(Line2D([0], [0], color=color, lw=4))
fig.legend(legend_list, THIOL, ncol=len(THIOL), loc="upper center",bbox_to_anchor=(0.5, 1.05))
fig1.legend(legend_list, THIOL, ncol=len(THIOL), loc="upper center",bbox_to_anchor=(0.5, 1.05))
fig2.legend(legend_list, THIOL, ncol=len(THIOL), loc="upper center",bbox_to_anchor=(0.5, 1.05))
fig3.legend(legend_list, THIOL, ncol=len(THIOL), loc="upper center",bbox_to_anchor=(0.5, 1.05))

fig.savefig(Path("../Graphs/SupplementaryFigure3_1.pdf"),format='pdf',dpi=500, bbox_inches='tight')
fig1.savefig(Path("../Graphs/SupplementaryFigure3_2.pdf"),format='pdf',dpi=500, bbox_inches='tight')
fig2.savefig(Path("../Graphs/SupplementaryFigure3_3.pdf"),format='pdf',dpi=500, bbox_inches='tight')
fig3.savefig(Path("../Graphs/SupplementaryFigure3_4.pdf"),format='pdf',dpi=500, bbox_inches='tight')

plt.show()