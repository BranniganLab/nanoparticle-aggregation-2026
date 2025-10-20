#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 12:44:40 2025

@author: jje63
"""

import argparse
from pathlib import Path, PurePath
import re

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def averagedata(data):
    avg_data = data.mean()
    return avg_data

def atoi(text):
    return int(text) if text.isdigit() else text

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def make_data(path):
    NP = sorted([file.name for file in path.iterdir() if file.is_file()], key=natural_keys)
    NPlist_xy = []
    NPlist_xyz = []
    NPlist_z = []
    for filename in NP:
        test = generalFileParse(filename, path)
        test.update_data()
        test.make_distances_XYZ()
        test.make_distances_XY()
        NPlist_xy.append(float(averagedata(test.data_frame["xydist"])))
        NPlist_xyz.append(float(averagedata(test.data_frame["xyzdist"])))
        NPlist_z.append(float(averagedata(np.abs(test.data_frame["z-val"]))))
    return [NPlist_xy, NPlist_xyz, NPlist_z]

class generalFileParse:
    def __init__(self, file_name, directory_path):
        self.directory_path = directory_path
        self.file_path = directory_path.joinpath(file_name)
        self.data_frame = pd.DataFrame()
        
    def update_data(self):
        if self.file_path.exists():
            data = np.loadtxt(self.file_path, comments=["#","@"])
            self.data_frame["z-val"] = data[:,3]
            self.data_frame["y-val"] = data[:,2]
            self.data_frame["x-val"] = data[:,1]
            self.data_frame['Time'] = data[:,0]
        else:
            raise ValueError("File doesn't exist")
            
    def make_distances_XYZ(self):
        summed_data = (self.data_frame["x-val"]**2) + (self.data_frame["y-val"]**2) + (self.data_frame["z-val"]**2)
        dist = np.sqrt(summed_data)
        self.data_frame["xyzdist"] = dist
        
    def make_distances_XY(self):
        summed_data = (self.data_frame["x-val"]**2) + (self.data_frame["y-val"]**2)
        dist = np.sqrt(summed_data)
        self.data_frame["xydist"] = dist
        
        
if __name__ == "__main__":
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

    figure, axs = plt.subplots(1,2, figsize=(24,8))
    axs[0].plot(hydravg_xy, hydravg_xyz, label="Hydrophobic (C5)", linewidth=2)
    axs[0].plot(hydravg_xy, hydravg_xy, label="Hydrophobic Y=X", linestyle="--", linewidth=1)
    axs[0].plot(polravg_xy, polravg_xyz, label="Polar (P5)", color="red", linewidth=2)
    axs[0].plot(polravg_xy, polravg_xy, label="Polar Y=X", linestyle="-.", linewidth=1)
    axs[0].set_ylabel(r"$\langle\sqrt{x^2+y^2+z^2}\rangle$",fontsize=20)
    axs[0].set_xlabel(r"$\langle\sqrt{x^2+y^2}\rangle$",fontsize=20)
    axs[0].legend()
    axs[0].tick_params(axis='both', labelsize=15)

    axs[1].plot(hydravg_xy[:indexhyd[0][0]], hydravg_z[:indexhyd[0][0]], label="Hydrophobic (C5)", linewidth=2)
    axs[1].fill_between(hydravg_xy[:indexhyd[0][0]],
                        hydravg_z[:indexhyd[0][0]]-hydrstd_z[:indexhyd[0][0]],
                        hydravg_z[:indexhyd[0][0]]+hydrstd_z[:indexhyd[0][0]],
                        alpha=0.5)
    axs[1].plot(polravg_xy[:indexpol[0][0]], polravg_z[:indexpol[0][0]], label="Polar (P5)", color="red", linewidth=2)
    axs[1].fill_between(polravg_xy[:indexpol[0][0]],
                        polravg_z[:indexpol[0][0]]-polrstd_z[:indexpol[0][0]],
                        polravg_z[:indexpol[0][0]]+polrstd_z[:indexpol[0][0]],
                        alpha=0.5)
    axs[1].set_ylabel(r"$\langle |z| \rangle$", fontsize=20)
    axs[1].set_xlabel(r"$\langle\sqrt{x^2+y^2}\rangle$ (nm)", fontsize=20)
    axs[1].legend(loc="upper left")
    axs[1].set_yticks(np.arange(0, 1.6, step=0.5))
    axs[1].set_xticks(np.arange(2.5, 5.1, step=0.5))
    axs[1].tick_params(axis='both', labelsize=15)


    plt.savefig(Path("/media/jje63/easystore1/GoldNanoparticleFE/GNP_US_All/sqrtsofdistance_final.pdf"),format='pdf',dpi=500, bbox_inches='tight')
    
