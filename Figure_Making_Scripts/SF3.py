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
import argparse
from matplotlib.lines import Line2D
sys.path.insert(0, "../Analysis/Figure_1_scripts/")
from SASAplotter import generalSASA, make_thiol_dataset, create_sasa_core_replica_data, create_sasa_full_replica_data
from order_density_contact_potter import generalFileParse, create_contact_core_replica_data, create_contact_full_replica_data,make_thiol_dataset_O_C


############### Draw Grid ##############

D1 = 50
D2 = 10
fig_C1,ax_C1 = plt.subplots(1,5, figsize=(D1,D2), layout='constrained', sharex=True)
fig_C5,ax_C5 = plt.subplots(1,5, figsize=(D1,D2), layout='constrained', sharex=True)
fig_N0,ax_N0 = plt.subplots(1,5, figsize=(D1,D2), layout='constrained', sharex=True)
fig_P1,ax_P1 = plt.subplots(1,5, figsize=(D1,D2), layout='constrained', sharex=True)
fig_P5,ax_P5 = plt.subplots(1,5, figsize=(D1,D2), layout='constrained', sharex=True)
fig_SS,ax_SS = plt.subplots(1,5, figsize=(D1,D2), layout='constrained', sharex=True)

Wat_SAS_plot = [fig_C1, fig_C5, fig_N0, fig_P1, fig_P5, fig_SS]
Wat_SAS_axes = [ax_C1, ax_C5, ax_N0, ax_P1, ax_P5, ax_SS]

fig1_C1,ax1_C1 = plt.subplots(1,5, figsize=(D1,D2), layout='constrained', sharex=True)
fig1_C5,ax1_C5 = plt.subplots(1,5, figsize=(D1,D2), layout='constrained', sharex=True)
fig1_N0,ax1_N0 = plt.subplots(1,5, figsize=(D1,D2), layout='constrained', sharex=True)
fig1_P1,ax1_P1 = plt.subplots(1,5, figsize=(D1,D2), layout='constrained', sharex=True)
fig1_P5,ax1_P5 = plt.subplots(1,5, figsize=(D1,D2), layout='constrained', sharex=True)
fig1_SS,ax1_SS = plt.subplots(1,5, figsize=(D1,D2), layout='constrained', sharex=True)

Lip_SAS_plot = [fig1_C1, fig1_C5, fig1_N0, fig1_P1, fig1_P5, fig1_SS]
Lip_SAS_axes = [ax1_C1, ax1_C5, ax1_N0, ax1_P1, ax1_P5, ax1_SS]

fig2_C1,ax2_C1 = plt.subplots(1,5, figsize=(D1,D2), layout='constrained', sharex=True)
fig2_C5,ax2_C5 = plt.subplots(1,5, figsize=(D1,D2), layout='constrained', sharex=True)
fig2_N0,ax2_N0 = plt.subplots(1,5, figsize=(D1,D2), layout='constrained', sharex=True)
fig2_P1,ax2_P1 = plt.subplots(1,5, figsize=(D1,D2), layout='constrained', sharex=True)
fig2_P5,ax2_P5 = plt.subplots(1,5, figsize=(D1,D2), layout='constrained', sharex=True)
fig2_SS,ax2_SS = plt.subplots(1,5, figsize=(D1,D2), layout='constrained', sharex=True)

Head_plot = [fig2_C1, fig2_C5, fig2_N0, fig2_P1, fig2_P5, fig2_SS]
Head_axes = [ax2_C1, ax2_C5, ax2_N0, ax2_P1, ax2_P5, ax2_SS]

fig3_C1,ax3_C1 = plt.subplots(1,5, figsize=(D1,D2), layout='constrained', sharex=True)
fig3_C5,ax3_C5 = plt.subplots(1,5, figsize=(D1,D2), layout='constrained', sharex=True)
fig3_N0,ax3_N0 = plt.subplots(1,5, figsize=(D1,D2), layout='constrained', sharex=True)
fig3_P1,ax3_P1 = plt.subplots(1,5, figsize=(D1,D2), layout='constrained', sharex=True)
fig3_P5,ax3_P5 = plt.subplots(1,5, figsize=(D1,D2), layout='constrained', sharex=True)
fig3_SS,ax3_SS = plt.subplots(1,5, figsize=(D1,D2), layout='constrained', sharex=True)

Tail_plot = [fig3_C1, fig3_C5, fig3_N0, fig3_P1, fig3_P5, fig3_SS]
Tail_axes = [ax3_C1, ax3_C5, ax3_N0, ax3_P1, ax3_P5, ax3_SS]

############# Making plottable Cluster Data #############
DIRECTORY_PATH = Path("../Simulation/Single_Nanoparticle")
CORETYPES = ["C1","C5","N0","P1","P5"]
CORETYPES2 = ["C1","C5","N0","P1","P5","SS"]
THIOL = ["Octanethiol","Dodecanethiol","Hexadecanethiol","Icosanethiol","Tetracosanethiol"]
REPLICA = ["Replica1","Replica2","Replica3"]
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
fs = 60

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
    
def plot_reps_2(combined_reps, figure_list, axes_list, data_name, ylabel): 
    for i,thiol in enumerate(THIOL):
        tempframe = pd.DataFrame()
        #print(combined_reps)
        tempframe["Replica1"] = combined_reps[0][thiol].rolling(window=30).mean()
        tempframe["Replica2"] = combined_reps[1][thiol].rolling(window=30).mean()
        tempframe["Replica3"] = combined_reps[2][thiol].rolling(window=30).mean()
        tempframe["Time"] = np.arange(len(combined_reps[0]))/100
        tempframe.plot(ax=axes_list[i],
                  x="Time",
                  y=["Replica1", "Replica2", "Replica3"],
                  title=thiol,
                  xlabel='',
                  legend=False,
                  fontsize=55,
                  linewidth=5)
        axes_list[i].set_title(thiol, fontsize=60)
    color_list = [line.get_color() for line in axes_list[i].lines]
    legend_list = []
    for color in color_list:
        legend_list.append(Line2D([0], [0], color=color, lw=4))
    figure_list.legend(legend_list, REPLICA, ncol=len(REPLICA), loc="upper center",bbox_to_anchor=(0.5, 1.20), fontsize=55)
    figure_list.supylabel(ylabel, fontsize=fs)
    figure_list.supxlabel(r'Time ($\mu s$)', fontsize=fs)
        

#### WASA #####
plot_reps_2(combine_replicas(C1data_wat), Wat_SAS_plot[0],Wat_SAS_axes[0],"C1", r'Water Accesible Surface Area($nm^{2}$)' )
plot_reps_2(combine_replicas(C5data_wat), Wat_SAS_plot[1],Wat_SAS_axes[1],"C5", r'Water Accesible Surface Area($nm^{2}$)' )
plot_reps_2(combine_replicas(N0data_wat), Wat_SAS_plot[2],Wat_SAS_axes[2],"N0", r'Water Accesible Surface Area($nm^{2}$)' )
plot_reps_2(combine_replicas(P1data_wat), Wat_SAS_plot[3],Wat_SAS_axes[3],"P1", r'Water Accesible Surface Area($nm^{2}$)' )
plot_reps_2(combine_replicas(P5data_wat), Wat_SAS_plot[4],Wat_SAS_axes[4],"P5", r'Water Accesible Surface Area($nm^{2}$)' )
plot_reps_2(combine_replicas(SSdata_wat), Wat_SAS_plot[5],Wat_SAS_axes[5],"SS", r'Water Accesible Surface Area($nm^{2}$)' )

for coretype,plot in zip(CORETYPES2,Wat_SAS_plot):
    plot.savefig(Path(f"../Graphs/SupplementaryFigureWASA_{coretype}.pdf"),format='pdf',dpi=500, bbox_inches='tight')
    plt.close(plot)
    
#### LASA #####
plot_reps_2(combine_replicas(C1data_lip), Lip_SAS_plot[0],Lip_SAS_axes[0],"C1", r'Lipid Accesible Surface Area($nm^{2}$)' )
plot_reps_2(combine_replicas(C5data_lip), Lip_SAS_plot[1],Lip_SAS_axes[1],"C5", r'Lipid Accesible Surface Area($nm^{2}$)' )
plot_reps_2(combine_replicas(N0data_lip), Lip_SAS_plot[2],Lip_SAS_axes[2],"N0", r'Lipid Accesible Surface Area($nm^{2}$)' )
plot_reps_2(combine_replicas(P1data_lip), Lip_SAS_plot[3],Lip_SAS_axes[3],"P1", r'Lipid Accesible Surface Area($nm^{2}$)' )
plot_reps_2(combine_replicas(P5data_lip), Lip_SAS_plot[4],Lip_SAS_axes[4],"P5", r'Lipid Accesible Surface Area($nm^{2}$)' )
plot_reps_2(combine_replicas(SSdata_lip), Lip_SAS_plot[5],Lip_SAS_axes[5],"SS", r'Lipid Accesible Surface Area($nm^{2}$)' )
for coretype,plot in zip(CORETYPES2,Lip_SAS_plot):
    plot.savefig(Path(f"../Graphs/SupplementaryFigureLASA_{coretype}.pdf"),format='pdf',dpi=500, bbox_inches='tight')
    plt.close(plot)

DT = "contact"

#### Head Contact #####
plot_reps_2(combine_replicas(C1data_head, DT), Head_plot[0],Head_axes[0],"C1", r'Number of Lipid Head Contacts' )
plot_reps_2(combine_replicas(C5data_head, DT), Head_plot[1],Head_axes[1],"C5", r'Number of Lipid Head Contacts' )
plot_reps_2(combine_replicas(N0data_head, DT), Head_plot[2],Head_axes[2],"N0", r'Number of Lipid Head Contacts' )
plot_reps_2(combine_replicas(P1data_head, DT), Head_plot[3],Head_axes[3],"P1", r'Number of Lipid Head Contacts' )
plot_reps_2(combine_replicas(P5data_head, DT), Head_plot[4],Head_axes[4],"P5", r'Number of Lipid Head Contacts' )
plot_reps_2(combine_replicas(SSdata_head, DT), Head_plot[5],Head_axes[5],"SS", r'Number of Lipid Head Contacts' )
for coretype,plot in zip(CORETYPES2,Head_plot):
    plot.savefig(Path(f"../Graphs/SupplementaryFigureHeadCont_{coretype}.pdf"),format='pdf',dpi=500, bbox_inches='tight')
    plt.close(plot)
    
#### Tail Contact #####
plot_reps_2(combine_replicas(C1data_tail, DT), Tail_plot[0],Tail_axes[0],"C1", r'Number of Lipid Tail Contacts' )
plot_reps_2(combine_replicas(C5data_tail, DT), Tail_plot[1],Tail_axes[1],"C5", r'Number of Lipid Tail Contacts' )
plot_reps_2(combine_replicas(N0data_tail, DT), Tail_plot[2],Tail_axes[2],"N0", r'Number of Lipid Tail Contacts' )
plot_reps_2(combine_replicas(P1data_tail, DT), Tail_plot[3],Tail_axes[3],"P1", r'Number of Lipid Tail Contacts' )
plot_reps_2(combine_replicas(P5data_tail, DT), Tail_plot[4],Tail_axes[4],"P5", r'Number of Lipid Tail Contacts' )
plot_reps_2(combine_replicas(SSdata_tail, DT), Tail_plot[5],Tail_axes[5],"SS", r'Number of Lipid Tail Contacts' )
for coretype,plot in zip(CORETYPES2,Tail_plot):
    plot.savefig(Path(f"../Graphs/SupplementaryFigureTailCont_{coretype}.pdf"),format='pdf',dpi=500, bbox_inches='tight')
    plt.close(plot)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-sp","--showplot", help="Show the plot", action='store_true')
    args = parser.parse_args()
    if args.showplot:
        plt.show()  