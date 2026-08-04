#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 09:34:48 2025

@author: jje63
"""

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

sys.path.insert(0, "../Analysis/Figure_1_scripts/")
from order_density_contact_potter import (
    create_contact_core_replica_data,
    create_contact_full_replica_data,
    make_thiol_dataset_O_C,
)
from SASAplotter import (
    create_sasa_core_replica_data,
    create_sasa_full_replica_data,
    make_thiol_dataset,
)

Pagelength = 4
Pagewidth = 9

############### Draw Grid ##############

# mosaic = [['ImgA','SASACoreW','SASALLW','AVGconthead'],
#          ['ImgB','SASACoreH','SASALLH','AVGconttail'],
#          ]
mosaic = [
    ["ImgA", "SASACoreW", "SASACoreH", "AVGconthead"],
    ["ImgB", "SASALLW", "SASALLH", "AVGconttail"],
]
fig = plt.figure(figsize=(Pagewidth, Pagelength), layout="tight")
ax = fig.subplot_mosaic(
    mosaic,
    width_ratios=[1.5, 1, 1, 1],
)
Annotation = ["A)", "B)", "C)", "D)", "E)", "F)", "G)", "H)"]

### side panel ###
fig.text(
    0.00,
    0.92,
    Annotation[0],
    # fontfamily='san-serif'
)
fig.text(
    0.00,
    0.45,
    Annotation[1],
    # fontfamily='san-serif'
)

fig.text(
    0.28,
    0.92,
    Annotation[2],
    # fontfamily='san-serif'
)
fig.text(
    0.28,
    0.45,
    Annotation[3],
    # fontfamily='san-serif'
)

fig.text(
    0.52,
    0.92,
    Annotation[4],
    # fontfamily='san-serif'
)
fig.text(
    0.52,
    0.45,
    Annotation[5],
    # fontfamily='san-serif'
)

fig.text(
    0.76,
    0.92,
    Annotation[6],
    # fontfamily='san-serif'
)
fig.text(
    0.76,
    0.45,
    Annotation[7],
    # fontfamily='san-serif'
)
############# Import Images #############
Figure1 = Path("../Media/Figure1/GNP_hyd.png")
Figure2 = Path("../Media/Figure1/GNP_pol.png")
Hydro = np.asarray(Image.open(Figure1))
Polar = np.asarray(Image.open(Figure2))

############# Plot on Grid #############
label_font = {  #'family': 'San-serif',
    "color": "black",
    "weight": "normal",
    "size": 8,
}
tick_font = {  #'family': 'San-serif',
    "color": "black",
    "weight": "normal",
    "size": 6,
}
LWidth = 1
LStyle = "solid"
MSize = 5
CSize = 4
Ligand_Lengths = [8, 12, 16, 20, 24]
hydrophobic_color = "#003dfc"
polar_color = "#fc8900"
softsphere_color = "grey"


################## Images ####################

ax["ImgA"].imshow(Hydro)
ax["ImgA"].set_aspect("auto")
ax["ImgA"].axis("off")

ax["ImgB"].imshow(Polar)
ax["ImgB"].set_aspect("auto")
ax["ImgB"].axis("off")

######## Water SASA #################

DIRECTORY_PATH = Path("../Simulation/Single_Nanoparticle")
CORETYPES = ["C1", "C5", "N0", "P1", "P5"]
CORETYPES2 = ["C1", "C5", "N0", "P1", "P5", "SS"]
THIOL = [
    "Octanethiol",
    "Dodecanethiol",
    "Hexadecanethiol",
    "Icosanethiol",
    "Tetracosanethiol",
]
# REPLICA = ["Replica1","Replica2","Replica3"]
LENGTHS = [2, 3, 4, 5, 6]
DATA_FILE = "watersasa" + ".dat"

C1data = make_thiol_dataset(DIRECTORY_PATH, "C1", "*thiol", "Replica*", DATA_FILE)
C1_replica_combined = create_sasa_core_replica_data(C1data)
C1_full_replica = create_sasa_full_replica_data(C1data)
C1AVG = C1_full_replica.mean(axis=1).iloc[0]
C1STD = C1_full_replica.std(axis=1).iloc[0] / np.sqrt(len(C1_full_replica.columns))

C5data = make_thiol_dataset(DIRECTORY_PATH, "C5", "*thiol", "Replica*", DATA_FILE)
C5_replica_combined = create_sasa_core_replica_data(C5data)
C5_full_replica = create_sasa_full_replica_data(C5data)
C5AVG = C5_full_replica.mean(axis=1).iloc[0]
C5STD = C5_full_replica.std(axis=1).iloc[0] / np.sqrt(len(C5_full_replica.columns))

N0data = make_thiol_dataset(DIRECTORY_PATH, "N0", "*thiol", "Replica*", DATA_FILE)
N0_replica_combined = create_sasa_core_replica_data(N0data)
N0_full_replica = create_sasa_full_replica_data(N0data)
N0AVG = N0_full_replica.mean(axis=1).iloc[0]
N0STD = N0_full_replica.std(axis=1).iloc[0] / np.sqrt(len(N0_full_replica.columns))

P1data = make_thiol_dataset(DIRECTORY_PATH, "P1", "*thiol", "Replica*", DATA_FILE)
P1_replica_combined = create_sasa_core_replica_data(P1data)
P1_full_replica = create_sasa_full_replica_data(P1data)
P1AVG = P1_full_replica.mean(axis=1).iloc[0]
P1STD = P1_full_replica.std(axis=1).iloc[0] / np.sqrt(len(P1_full_replica.columns))

P5data = make_thiol_dataset(DIRECTORY_PATH, "P5", "*thiol", "Replica*", DATA_FILE)
P5_replica_combined = create_sasa_core_replica_data(P5data)
P5_full_replica = create_sasa_full_replica_data(P5data)
P5AVG = P5_full_replica.mean(axis=1).iloc[0]
P5STD = P5_full_replica.std(axis=1).iloc[0] / np.sqrt(len(P5_full_replica.columns))

SSdata = make_thiol_dataset(DIRECTORY_PATH, "SS", "*thiol", "Replica*", DATA_FILE)
SS_replica_combined = create_sasa_core_replica_data(SSdata)
SS_full_replica = create_sasa_full_replica_data(SSdata)
SSAVG = SS_full_replica.mean(axis=1).iloc[0]
SSSTD = SS_full_replica.std(axis=1).iloc[0] / np.sqrt(len(SS_full_replica.columns))

Cores = [
    C1_replica_combined,
    C5_replica_combined,
    N0_replica_combined,
    P1_replica_combined,
    P5_replica_combined,
    SS_replica_combined,
]

for i, core in enumerate(Cores):
    Data = [
        core[THIOL[0]].iloc[0],
        core[THIOL[1]].iloc[0],
        core[THIOL[2]].iloc[0],
        core[THIOL[3]].iloc[0],
        core[THIOL[4]].iloc[0],
    ]
    STDData = [
        core[THIOL[0]].iloc[1],
        core[THIOL[1]].iloc[1],
        core[THIOL[2]].iloc[1],
        core[THIOL[3]].iloc[1],
        core[THIOL[4]].iloc[1],
    ]
    ax["SASACoreW"].errorbar(
        LENGTHS,
        Data,
        yerr=STDData,
        capsize=CSize,
        elinewidth=1,
        capthick=0.5,
        fmt="-o",
        label=CORETYPES2[i],
        linewidth=LWidth,
        markersize=MSize,
    )
ax["SASACoreW"].set_xticks(LENGTHS)
ax["SASACoreW"].set_xticklabels(LENGTHS, fontdict=tick_font)
ax["SASACoreW"].set_yticks(np.arange(0, 180, step=40))
ax["SASACoreW"].set_yticklabels(np.arange(0, 180, step=40), fontdict=tick_font)
ax["SASACoreW"].set_xlabel("Ligand Length", fontdict=label_font)
ax["SASACoreW"].set_ylabel(r"Water SASA (nm$^{2}$)", fontdict=label_font)
# ax['SASACoreW'].tick_params(axis='both', labelsize=20)
ax["SASACoreW"].legend(prop={"size": 4}, markerscale=0.5, ncol=2)

for i, thiol in enumerate(THIOL):
    coreplot = [
        Cores[0][thiol].iloc[0],
        Cores[1][thiol].iloc[0],
        Cores[2][thiol].iloc[0],
        Cores[3][thiol].iloc[0],
        Cores[4][thiol].iloc[0],
        # Cores[5][thiol].iloc[0],
        # Cores[6][thiol].iloc[0]
    ]
    cpss = Cores[5][thiol].iloc[0]
    coreplotstd = [
        Cores[0][thiol].iloc[1],
        Cores[1][thiol].iloc[1],
        Cores[2][thiol].iloc[1],
        Cores[3][thiol].iloc[1],
        Cores[4][thiol].iloc[1],
        # Cores[5][thiol].iloc[1],
        # Cores[6][thiol].iloc[1]
    ]
    cpssstd = Cores[5][thiol].iloc[1]
    line = ax["SASALLW"].errorbar(
        CORETYPES2[0:-1],
        coreplot,
        yerr=coreplotstd,
        capsize=CSize,
        elinewidth=1,
        capthick=0.5,
        fmt="-o",
        label=i + 2,
        linewidth=LWidth,
        markersize=MSize,
    )
    ax["SASALLW"].errorbar(
        CORETYPES2[-1],
        cpss,
        yerr=cpssstd,
        capsize=CSize,
        elinewidth=1,
        capthick=0.5,
        fmt="-o",
        label="",
        color=line.lines[0].get_color(),
        linewidth=LWidth,
        markersize=MSize,
    )
ax["SASALLW"].set_xticks([0, 1, 2, 3, 4, 5])
ax["SASALLW"].set_xticklabels(CORETYPES2, fontdict=tick_font)
ax["SASALLW"].set_yticks(np.arange(0, 180, step=40))
ax["SASALLW"].set_yticklabels(np.arange(0, 180, step=40), fontdict=tick_font)
ax["SASALLW"].set_xlabel("Core Parameter", fontdict=label_font)
ax["SASALLW"].set_ylabel(r"Water SASA (nm$^{2}$)", fontdict=label_font)
ax["SASALLW"].legend(prop={"size": 4}, markerscale=0.5, ncol=2)

######## Lipid SASA #################

DATA_FILE = "lipidsasa" + ".dat"

C1data = make_thiol_dataset(DIRECTORY_PATH, "C1", "*thiol", "Replica*", DATA_FILE)
C1_replica_combined = create_sasa_core_replica_data(C1data)
C1_full_replica = create_sasa_full_replica_data(C1data)
C1AVG = C1_full_replica.mean(axis=1).iloc[0]
C1STD = C1_full_replica.std(axis=1).iloc[0] / np.sqrt(len(C1_full_replica.columns))

C5data = make_thiol_dataset(DIRECTORY_PATH, "C5", "*thiol", "Replica*", DATA_FILE)
C5_replica_combined = create_sasa_core_replica_data(C5data)
C5_full_replica = create_sasa_full_replica_data(C5data)
C5AVG = C5_full_replica.mean(axis=1).iloc[0]
C5STD = C5_full_replica.std(axis=1).iloc[0] / np.sqrt(len(C5_full_replica.columns))

N0data = make_thiol_dataset(DIRECTORY_PATH, "N0", "*thiol", "Replica*", DATA_FILE)
N0_replica_combined = create_sasa_core_replica_data(N0data)
N0_full_replica = create_sasa_full_replica_data(N0data)
N0AVG = N0_full_replica.mean(axis=1).iloc[0]
N0STD = N0_full_replica.std(axis=1).iloc[0] / np.sqrt(len(N0_full_replica.columns))

P1data = make_thiol_dataset(DIRECTORY_PATH, "P1", "*thiol", "Replica*", DATA_FILE)
P1_replica_combined = create_sasa_core_replica_data(P1data)
P1_full_replica = create_sasa_full_replica_data(P1data)
P1AVG = P1_full_replica.mean(axis=1).iloc[0]
P1STD = P1_full_replica.std(axis=1).iloc[0] / np.sqrt(len(P1_full_replica.columns))

P5data = make_thiol_dataset(DIRECTORY_PATH, "P5", "*thiol", "Replica*", DATA_FILE)
P5_replica_combined = create_sasa_core_replica_data(P5data)
P5_full_replica = create_sasa_full_replica_data(P5data)
P5AVG = P5_full_replica.mean(axis=1).iloc[0]
P5STD = P5_full_replica.std(axis=1).iloc[0] / np.sqrt(len(P5_full_replica.columns))

SSdata = make_thiol_dataset(DIRECTORY_PATH, "SS", "*thiol", "Replica*", DATA_FILE)
SS_replica_combined = create_sasa_core_replica_data(SSdata)
SS_full_replica = create_sasa_full_replica_data(SSdata)
SSAVG = SS_full_replica.mean(axis=1).iloc[0]
SSSTD = SS_full_replica.std(axis=1).iloc[0] / np.sqrt(len(SS_full_replica.columns))

Cores = [
    C1_replica_combined,
    C5_replica_combined,
    N0_replica_combined,
    P1_replica_combined,
    P5_replica_combined,
    SS_replica_combined,
]

for i, core in enumerate(Cores):
    Data = [
        core[THIOL[0]].iloc[0],
        core[THIOL[1]].iloc[0],
        core[THIOL[2]].iloc[0],
        core[THIOL[3]].iloc[0],
        core[THIOL[4]].iloc[0],
    ]
    STDData = [
        core[THIOL[0]].iloc[1],
        core[THIOL[1]].iloc[1],
        core[THIOL[2]].iloc[1],
        core[THIOL[3]].iloc[1],
        core[THIOL[4]].iloc[1],
    ]
    ax["SASACoreH"].errorbar(
        LENGTHS,
        Data,
        yerr=STDData,
        capsize=CSize,
        elinewidth=1,
        capthick=0.5,
        fmt="-o",
        label=CORETYPES2[i],
        linewidth=LWidth,
        markersize=MSize,
    )
ax["SASACoreH"].set_xticks(LENGTHS)
ax["SASACoreH"].set_xticklabels(LENGTHS, fontdict=tick_font)
ax["SASACoreH"].set_yticks(np.arange(0, 180, step=40))
ax["SASACoreH"].set_yticklabels(np.arange(0, 180, step=40), fontdict=tick_font)
ax["SASACoreH"].set_xlabel("Ligand Length", fontdict=label_font)
ax["SASACoreH"].set_ylabel(r"Lipid SASA (nm$^{2}$)", fontdict=label_font)
ax["SASACoreH"].legend(prop={"size": 4}, markerscale=0.5, ncol=2)

for i, thiol in enumerate(THIOL):
    coreplot = [
        Cores[0][thiol].iloc[0],
        Cores[1][thiol].iloc[0],
        Cores[2][thiol].iloc[0],
        Cores[3][thiol].iloc[0],
        Cores[4][thiol].iloc[0],
        # Cores[5][thiol].iloc[0],
        # Cores[6][thiol].iloc[0]
    ]
    cpss = Cores[5][thiol].iloc[0]
    coreplotstd = [
        Cores[0][thiol].iloc[1],
        Cores[1][thiol].iloc[1],
        Cores[2][thiol].iloc[1],
        Cores[3][thiol].iloc[1],
        Cores[4][thiol].iloc[1],
        # Cores[5][thiol].iloc[1],
        # Cores[6][thiol].iloc[1]
    ]
    cpssstd = Cores[5][thiol].iloc[1]
    line = ax["SASALLH"].errorbar(
        CORETYPES2[0:-1],
        coreplot,
        yerr=coreplotstd,
        capsize=CSize,
        elinewidth=1,
        capthick=0.5,
        fmt="-o",
        label=i + 2,
        linewidth=LWidth,
        markersize=MSize,
    )
    ax["SASALLH"].errorbar(
        CORETYPES2[-1],
        cpss,
        yerr=cpssstd,
        capsize=CSize,
        elinewidth=1,
        capthick=0.5,
        fmt="-o",
        label="",
        color=line.lines[0].get_color(),
        linewidth=LWidth,
        markersize=MSize,
    )
ax["SASALLH"].set_xticks([0, 1, 2, 3, 4, 5])
ax["SASALLH"].set_xticklabels(CORETYPES2, fontdict=tick_font)
ax["SASALLH"].set_yticks(np.arange(0, 180, step=40))
ax["SASALLH"].set_yticklabels(np.arange(0, 180, step=40), fontdict=tick_font)
ax["SASALLH"].set_xlabel("Core Parameter", fontdict=label_font)
ax["SASALLH"].set_ylabel(r"Lipid SASA (nm$^{2}$)", fontdict=label_font)
ax["SASALLH"].legend(prop={"size": 4}, markerscale=0.5, ncol=2)

######## Lipid Head Contact #################

DATA_FILE = "headcont" + ".dat"

C1datacont = make_thiol_dataset_O_C(
    DIRECTORY_PATH, "C1", "*thiol", "Replica*", DATA_FILE, "contact"
)
C1_replica_combined = create_contact_core_replica_data(C1datacont)
C1_full_replica = create_contact_full_replica_data(C1datacont)
C1AVG = C1_full_replica.mean(axis=1).iloc[0]
C1STD = C1_full_replica.std(axis=1).iloc[0] / np.sqrt(len(C1_full_replica.columns))

C5datacont = make_thiol_dataset_O_C(
    DIRECTORY_PATH, "C5", "*thiol", "Replica*", DATA_FILE, "contact"
)
C5_replica_combined = create_contact_core_replica_data(C5datacont)
C5_full_replica = create_contact_full_replica_data(C5datacont)
C5AVG = C5_full_replica.mean(axis=1).iloc[0]
C5STD = C5_full_replica.std(axis=1).iloc[0] / np.sqrt(len(C5_full_replica.columns))

N0datacont = make_thiol_dataset_O_C(
    DIRECTORY_PATH, "N0", "*thiol", "Replica*", DATA_FILE, "contact"
)
N0_replica_combined = create_contact_core_replica_data(N0datacont)
N0_full_replica = create_contact_full_replica_data(N0datacont)
N0AVG = N0_full_replica.mean(axis=1).iloc[0]
N0STD = N0_full_replica.std(axis=1).iloc[0] / np.sqrt(len(N0_full_replica.columns))

P1datacont = make_thiol_dataset_O_C(
    DIRECTORY_PATH, "P1", "*thiol", "Replica*", DATA_FILE, "contact"
)
P1_replica_combined = create_contact_core_replica_data(P1datacont)
P1_full_replica = create_contact_full_replica_data(P1datacont)
P1AVG = P1_full_replica.mean(axis=1).iloc[0]
P1STD = P1_full_replica.std(axis=1).iloc[0] / np.sqrt(len(P1_full_replica.columns))

P5datacont = make_thiol_dataset_O_C(
    DIRECTORY_PATH, "P5", "*thiol", "Replica*", DATA_FILE, "contact"
)
P5_replica_combined = create_contact_core_replica_data(P5datacont)
P5_full_replica = create_contact_full_replica_data(P5datacont)
P5AVG = P5_full_replica.mean(axis=1).iloc[0]
P5STD = P5_full_replica.std(axis=1).iloc[0] / np.sqrt(len(P5_full_replica.columns))

SSdatacont = make_thiol_dataset_O_C(
    DIRECTORY_PATH, "SS", "*thiol", "Replica*", DATA_FILE, "contact"
)
SS_replica_combined = create_contact_core_replica_data(SSdatacont)
SS_full_replica = create_contact_full_replica_data(SSdatacont)
SSAVG = SS_full_replica.mean(axis=1).iloc[0]
SSSTD = SS_full_replica.std(axis=1).iloc[0] / np.sqrt(len(SS_full_replica.columns))

Cores = [
    C1_replica_combined,
    C5_replica_combined,
    N0_replica_combined,
    P1_replica_combined,
    P5_replica_combined,
    SS_replica_combined,
]

ax["AVGconthead"].errorbar(
    CORETYPES,
    [C1AVG, C5AVG, N0AVG, P1AVG, P5AVG],
    yerr=[C1STD, C5STD, N0STD, P1STD, P5STD],
    fmt="-o",
    capsize=CSize,
    elinewidth=1,
    capthick=1,
    color="black",
    linewidth=LWidth,
    markersize=MSize,
)
ax["AVGconthead"].errorbar(
    "SS",
    SSAVG,
    yerr=SSSTD,
    fmt="-o",
    capsize=CSize,
    elinewidth=1,
    capthick=1,
    color="Orange",
    markersize=MSize,
)
ax["AVGconthead"].set_xlabel("Core Parameter", fontdict=label_font)
ax["AVGconthead"].set_ylabel(r"Average Contacts", fontdict=label_font)
ax["AVGconthead"].set_xticks([0, 1, 2, 3, 4, 5])
ax["AVGconthead"].set_xticklabels(CORETYPES2, fontdict=tick_font)
ax["AVGconthead"].set_yticks(np.arange(0, 12, step=2))
ax["AVGconthead"].set_yticklabels(np.arange(0, 12, step=2), fontdict=tick_font)

######## Lipid Tail Contact #################

DATA_FILE = "tailcont" + ".dat"

C1datacont = make_thiol_dataset_O_C(
    DIRECTORY_PATH, "C1", "*thiol", "Replica*", DATA_FILE, "contact"
)
C1_replica_combined = create_contact_core_replica_data(C1datacont)
C1_full_replica = create_contact_full_replica_data(C1datacont)
C1AVG = C1_full_replica.mean(axis=1).iloc[0]
C1STD = C1_full_replica.std(axis=1).iloc[0] / np.sqrt(len(C1_full_replica.columns))

C5datacont = make_thiol_dataset_O_C(
    DIRECTORY_PATH, "C5", "*thiol", "Replica*", DATA_FILE, "contact"
)
C5_replica_combined = create_contact_core_replica_data(C5datacont)
C5_full_replica = create_contact_full_replica_data(C5datacont)
C5AVG = C5_full_replica.mean(axis=1).iloc[0]
C5STD = C5_full_replica.std(axis=1).iloc[0] / np.sqrt(len(C5_full_replica.columns))

N0datacont = make_thiol_dataset_O_C(
    DIRECTORY_PATH, "N0", "*thiol", "Replica*", DATA_FILE, "contact"
)
N0_replica_combined = create_contact_core_replica_data(N0datacont)
N0_full_replica = create_contact_full_replica_data(N0datacont)
N0AVG = N0_full_replica.mean(axis=1).iloc[0]
N0STD = N0_full_replica.std(axis=1).iloc[0] / np.sqrt(len(N0_full_replica.columns))

P1datacont = make_thiol_dataset_O_C(
    DIRECTORY_PATH, "P1", "*thiol", "Replica*", DATA_FILE, "contact"
)
P1_replica_combined = create_contact_core_replica_data(P1datacont)
P1_full_replica = create_contact_full_replica_data(P1datacont)
P1AVG = P1_full_replica.mean(axis=1).iloc[0]
P1STD = P1_full_replica.std(axis=1).iloc[0] / np.sqrt(len(P1_full_replica.columns))

P5datacont = make_thiol_dataset_O_C(
    DIRECTORY_PATH, "P5", "*thiol", "Replica*", DATA_FILE, "contact"
)
P5_replica_combined = create_contact_core_replica_data(P5datacont)
P5_full_replica = create_contact_full_replica_data(P5datacont)
P5AVG = P5_full_replica.mean(axis=1).iloc[0]
P5STD = P5_full_replica.std(axis=1).iloc[0] / np.sqrt(len(P5_full_replica.columns))

SSdatacont = make_thiol_dataset_O_C(
    DIRECTORY_PATH, "SS", "*thiol", "Replica*", DATA_FILE, "contact"
)
SS_replica_combined = create_contact_core_replica_data(SSdatacont)
SS_full_replica = create_contact_full_replica_data(SSdatacont)
SSAVG = SS_full_replica.mean(axis=1).iloc[0]
SSSTD = SS_full_replica.std(axis=1).iloc[0] / np.sqrt(len(SS_full_replica.columns))

Cores = [
    C1_replica_combined,
    C5_replica_combined,
    N0_replica_combined,
    P1_replica_combined,
    P5_replica_combined,
    SS_replica_combined,
]

ax["AVGconttail"].errorbar(
    CORETYPES,
    [C1AVG, C5AVG, N0AVG, P1AVG, P5AVG],
    yerr=[C1STD, C5STD, N0STD, P1STD, P5STD],
    fmt="-o",
    capsize=CSize,
    elinewidth=1,
    capthick=1,
    color="black",
    linewidth=LWidth,
    markersize=MSize,
)
ax["AVGconttail"].errorbar(
    "SS",
    SSAVG,
    yerr=SSSTD,
    fmt="-o",
    capsize=CSize,
    elinewidth=1,
    capthick=1,
    color="Orange",
    markersize=MSize,
)
ax["AVGconttail"].set_xlabel("Core Parameter", fontdict=label_font)
ax["AVGconttail"].set_ylabel(r"Average Contacts", fontdict=label_font)
ax["AVGconttail"].set_xticks([0, 1, 2, 3, 4, 5])
ax["AVGconttail"].set_xticklabels(CORETYPES2, fontdict=tick_font)
ax["AVGconttail"].set_yticks(np.arange(0, 35, step=5))
ax["AVGconttail"].set_yticklabels(np.arange(0, 35, step=5), fontdict=tick_font)
fig.savefig(Path("../Graphs/Figure1.pdf"), format="pdf", dpi=500, bbox_inches="tight")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-sp", "--showplot", help="Show the plot", action="store_true")
    args = parser.parse_args()
    if args.showplot:
        plt.show()
