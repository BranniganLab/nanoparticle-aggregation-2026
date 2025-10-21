#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 09:30:40 2025

@author: jje63
"""

import sys
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
sys.path.insert(0, "../Analysis/Figure_2_scripts/")
from generalxvgplotter import generalFE 
from npdistance import generalFileParse, make_data, find_nearest

Pagelength = 6
Pagewidth = 6.5

############### Draw Grid ##############

mosaic = [['PMF','difPMF','Z-height'],
          ['dimerimg','dimerimg','dimerimg'],
          ['memimg','memimg','memimg']]
fig = plt.figure(figsize=(Pagewidth,Pagelength),
                 layout="constrained")
ax = fig.subplot_mosaic(mosaic,
                        height_ratios=[1.5, 2.5,1.75],
                        #gridspec_kw={"wspace": 0.5}
                        )
Annotation = ['a)','b)','c)']
Annotation_P2 = ['2.5 nm','3 nm', '5.5 nm', '8 nm']
Annotation_P3 = ['C5','P5']

### side panel ###
fig.text(
    0.04,
    0.99,
    Annotation[0],
    )

fig.text(
    0.04,
    0.66,
    Annotation[1],
    )

fig.text(
    0.04,
    0.26,
    Annotation[2],
    )

fig.text(
    0.04,
    0.57,
    Annotation_P3[0],
    )

fig.text(
    0.04,
    0.38,
    Annotation_P3[1],
    )

fig.text(
    0.04,
    0.20,
    Annotation_P3[0],
    )

fig.text(
    0.04,
    0.08,
    Annotation_P3[1],
    )

### Over Graph text ###
fig.text(
    0.18,
    0.66,
    Annotation_P2[0],
    )
fig.text(
    0.42,
    0.66,
    Annotation_P2[1],
    )

fig.text(
    0.63,
    0.66,
    Annotation_P2[2],
    )

fig.text(
    0.86,
    0.66,
    Annotation_P2[3],
    )

fig.text(
    0.42,
    0.26,
    Annotation_P3[0],
    )

fig.text(
    0.63,
    0.26,
    Annotation_P3[1],
    )
############# Import Images #############
Figure4 = Path("../Media/Figure2/Fig2image.png")
Figure5 = Path("../Media/Figure2/Fig2image_2.png")
dimerimg = np.asarray(Image.open(Figure4))
membimg = np.asarray(Image.open(Figure5))

############# Plot on Grid #############
my_font = {'family': 'serif',
           'color':  'black',
           'weight': 'normal',
           'size': 8}
LWidth = 1
LStyle = 'solid'
MSize = 5
CSize = 4 
Ligand_Lengths = [8,12,16,20,24]
hydrophobic_color = "#003dfc"
polar_color = "#fc8900"
softsphere_color = "grey"


    ################## Images ####################
    
ax['dimerimg'].imshow(dimerimg)
ax['dimerimg'].set_aspect('auto')
ax['dimerimg'].axis('off')

ax['memimg'].imshow(membimg)
ax['memimg'].set_aspect('auto')
ax['memimg'].axis('off')
    
    ############## PMF plot #######################

Mainpath = Path("../Simulation/Multi_Nanoparticle/Dimer_Free_Energy_System")
xvg1 = generalFE("profile.xvg", Mainpath.joinpath("Polar/GNP_US") , "xvg1")
xvg1.update_FE_data()
xvg1.apply_correction("3D")
xvg1.shift_zero_to_fe_plateau()

xvg2 = generalFE("profile.xvg", Mainpath.joinpath("Polar/GNP_US_2/GNP_US") , "xvg1")
xvg2.update_FE_data()
xvg2.apply_correction("3D")
xvg2.shift_zero_to_fe_plateau()

xvg3 = generalFE("profile.xvg", Mainpath.joinpath("Polar/GNP_US_3/GNP_US") , "xvg1")
xvg3.update_FE_data()
xvg3.apply_correction("3D")
xvg3.shift_zero_to_fe_plateau()

xvg4 = generalFE("profile.xvg", Mainpath.joinpath("Hydrophobic/GNP_US_hyd") , "xvg1")
xvg4.update_FE_data()
xvg4.apply_correction("3D")
xvg4.shift_zero_to_fe_plateau()

xvg5 = generalFE("profile.xvg", Mainpath.joinpath("Hydrophobic/GNP_US_hyd_2/GNP_US_hyd") , "xvg1")
xvg5.update_FE_data()
xvg5.apply_correction("3D")
xvg5.shift_zero_to_fe_plateau()

xvg6 = generalFE("profile.xvg",  Mainpath.joinpath("Hydrophobic/GNP_US_hyd_3/GNP_US_hyd") , "xvg1")
xvg6.update_FE_data()
xvg6.apply_correction("3D")
xvg6.shift_zero_to_fe_plateau()

dfstack = np.stack((np.array(xvg1.fe_data_frame["Values"][:-10]), np.array(xvg2.fe_data_frame["Values"][:-10]), np.array(xvg3.fe_data_frame["Values"][:-10])))
dfmean = np.mean(dfstack, axis=0)
dfstd = np.std(dfstack, axis=0)/np.sqrt(3)

dfstackhyd = np.stack((np.array(xvg4.fe_data_frame["Values"][:-10]), np.array(xvg5.fe_data_frame["Values"][:-10]), np.array(xvg6.fe_data_frame["Values"][:-10])))
dfmeanhyd = np.mean(dfstackhyd, axis=0)
dfstdhyd = np.std(dfstackhyd, axis=0)/np.sqrt(3)

ax['PMF'].plot(xvg4.fe_data_frame["CV"][:-10],
             dfmeanhyd,
             linewidth=LWidth,
             label="Hydrophobic(C5)")
ax['PMF'].plot(xvg1.fe_data_frame["CV"][:-10],
             dfmean,
             linewidth=LWidth,
             label="Polar(P5)")

ax['PMF'].fill_between(xvg4.fe_data_frame["CV"][:-10],
                    dfmeanhyd-dfstdhyd,
                    dfmeanhyd+dfstdhyd,
                    alpha=0.5)
ax['PMF'].fill_between(xvg1.fe_data_frame["CV"][:-10],
                    dfmean-dfstd,
                    dfmean+dfstd,
                    alpha=0.5)

ax['PMF'].axhline(y = 0, color="black", linestyle = ':')
ax['PMF'].set_yticks(np.arange(-115, 15, step=50))
ax['PMF'].set_xticks(np.arange(2, 12, step=2))
ax['PMF'].set_yticklabels(np.arange(-115, 15, step=50),fontdict=my_font)
ax['PMF'].set_xticklabels(np.arange(2, 12, step=2),fontdict=my_font)
ax['PMF'].set_ylabel("PMF (kJ $mol^{-1}$)", fontdict=my_font)
ax['PMF'].set_xlabel("r (nm)", fontdict=my_font)
ax['PMF'].legend(loc="lower right",fontsize='xx-small')

    ############## diff PMF plot #######################
diff = dfmeanhyd - dfmean 

ax['difPMF'].plot(xvg4.fe_data_frame["CV"][:-10],
            diff,
            color='grey',
            linewidth=LWidth)

ax['difPMF'].set_yticks(np.arange(-30, 30, step=10))
ax['difPMF'].set_xticks(np.arange(2, 12, step=2))
ax['difPMF'].set_yticklabels(np.arange(-30, 30, step=10),fontdict=my_font)
ax['difPMF'].set_xticklabels(np.arange(2, 12, step=2),fontdict=my_font)
ax['difPMF'].axhline(y = 0, color="black", linestyle = ':')
ax['difPMF'].set_ylabel(r'$\Delta PMF$ ' "(kJ $mol^{-1}$)",fontdict=my_font)
ax['difPMF'].set_xlabel("r (nm)",fontdict=my_font)


    ############## Z-distance plot #######################
hydropath1 = Path("/media/jje63/easystore1/GoldNanoparticleFE/GNP_US_All/Hydrophobic/GNP_US_hyd/NPdistance")
hydropath2 = Path("/media/jje63/easystore1/GoldNanoparticleFE/GNP_US_All/Hydrophobic/GNP_US_hyd_2/GNP_US_hyd/NPdistance")
hydropath3 = Path("/media/jje63/easystore1/GoldNanoparticleFE/GNP_US_All/Hydrophobic/GNP_US_hyd_3/GNP_US_hyd/NPdistance")

polarpath1 = Path("/media/jje63/easystore1/GoldNanoparticleFE/GNP_US_All/Polar/GNP_US/NPdistance")
polarpath2 = Path("/media/jje63/easystore1/GoldNanoparticleFE/GNP_US_All/Polar/GNP_US_2/GNP_US/NPdistance")
polarpath3 = Path("/media/jje63/easystore1/GoldNanoparticleFE/GNP_US_All/Polar/GNP_US_3/GNP_US/NPdistance")

hydrop1 = make_data(hydropath1)
hydrop2 = make_data(hydropath2)
hydrop3 = make_data(hydropath3)

polarp1 = make_data(polarpath1)
polarp2 = make_data(polarpath2)
polarp3 = make_data(polarpath3)


hydravg_z = np.mean([hydrop1[2],hydrop2[2],hydrop3[2][:-1]], axis=0)
hydrstd_z = np.std([hydrop1[2],hydrop2[2],hydrop3[2][:-1]], axis=0)

hydravg_xy = np.mean([hydrop1[0],hydrop2[0],hydrop3[0][:-1]], axis=0)
hydravg_xyz = np.mean([hydrop1[1],hydrop2[1],hydrop3[1][:-1]], axis=0)
nearhyd = find_nearest(hydravg_xy, value=5)
indexhyd = np.where(hydravg_xy == nearhyd)

polravg_z = np.mean([polarp1[2][:-1],polarp2[2][:-1],polarp3[2]], axis=0)
polrstd_z = np.std([polarp1[2][:-1],polarp2[2][:-1],polarp3[2]], axis=0)

polravg_xy = np.mean([polarp1[0][:-1],polarp2[0][:-1],polarp3[0]], axis=0)
polravg_xyz = np.mean([polarp1[1][:-1],polarp2[1][:-1],polarp3[1]], axis=0)
nearpol = find_nearest(polravg_xy, value=5)
indexpol = np.where(polravg_xy == nearpol)

ax['Z-height'].plot(hydravg_xy[:indexhyd[0][0]], 
                    hydravg_z[:indexhyd[0][0]], 
                    label="Hydrophobic (C5)", 
                    linewidth=LWidth)
ax['Z-height'].fill_between(hydravg_xy[:indexhyd[0][0]],
                        hydravg_z[:indexhyd[0][0]]-hydrstd_z[:indexhyd[0][0]],
                        hydravg_z[:indexhyd[0][0]]+hydrstd_z[:indexhyd[0][0]],
                        alpha=0.5)
ax['Z-height'].plot(polravg_xy[:indexpol[0][0]], 
                    polravg_z[:indexpol[0][0]], 
                    label="Polar (P5)", color="red", 
                    linewidth=LWidth)
ax['Z-height'].fill_between(polravg_xy[:indexpol[0][0]],
                        polravg_z[:indexpol[0][0]]-polrstd_z[:indexpol[0][0]],
                        polravg_z[:indexpol[0][0]]+polrstd_z[:indexpol[0][0]],
                        alpha=0.5)
ax['Z-height'].set_ylabel(r"$\langle |z| \rangle$",fontdict=my_font)
ax['Z-height'].set_xlabel(r"$\langle\sqrt{x^2+y^2}\rangle$ (nm)",fontdict=my_font)
ax['Z-height'].legend(loc="upper left")
ax['Z-height'].set_yticks(np.arange(0, 1.6, step=0.5))
ax['Z-height'].set_xticks(np.arange(2.5, 5.1, step=0.5))
ax['Z-height'].set_yticklabels(np.arange(0, 1.6, step=0.5),fontdict=my_font)
ax['Z-height'].set_xticklabels(np.arange(2.5, 5.1, step=0.5),fontdict=my_font)
ax['Z-height'].legend(loc="upper left",fontsize='xx-small')
fig.savefig(Path("../Graphs/Figure2.pdf"),format='pdf',dpi=500, bbox_inches='tight')
plt.show()