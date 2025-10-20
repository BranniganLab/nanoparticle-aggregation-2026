#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 07:53:53 2024

@author: jje63
"""

import argparse
from pathlib import Path, PurePath

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


KB = (1.3806452*(10**-23)*(6.022*(10**23)))*(10**-3)
R = 8.314462*(10**-3)
TEMP = 298.15 

class generalFE:
    def __init__(self, file_name, directory_path, data_name):
        self.directory_path = directory_path
        self.file_path = directory_path.joinpath(file_name)
        self.fe_data_frame = pd.DataFrame()
        self.data_name = data_name
        self.pmf_hist_file_name = file_name
        self.abf_hist_data = None
        
    def update_FE_data(self):
        if self.file_path.exists():
            fe_data = np.loadtxt(self.file_path, comments=["#","@"])
            self.fe_data_frame["Values"] = fe_data[:,1]
            self.fe_data_frame['CV'] = fe_data[:,0]
        else:
            raise ValueError("File doesn't exist")

    def apply_correction(self, dimension):
        if dimension == '2D':
            self.fe_data_frame["Values"] = self.fe_data_frame["Values"]-(-KB*TEMP*np.log(self.fe_data_frame["CV"]))
        if dimension == '3D':
            self.fe_data_frame["Values"] = self.fe_data_frame["Values"]-(-2*KB*TEMP*np.log(self.fe_data_frame["CV"]))
            
    def shift_zero_to_fe_plateau(self,slice1=-10,slice2=-8):
        plateau = np.average(self.fe_data_frame["Values"].iloc[slice1:slice2])
        self.fe_data_frame["Values"] = self.fe_data_frame["Values"] - plateau
        
if __name__=="main":
    xvg1 = generalFE("profile.xvg", Path("/media/jje63/easystore/GoldNanoparticleFE/GNP_US_All/Polar/GNP_US") , "xvg1")
    xvg1.update_FE_data()
    xvg1.apply_correction("3D")
    xvg1.shift_zero_to_fe_plateau()

    xvg2 = generalFE("profile.xvg", Path("/media/jje63/easystore/GoldNanoparticleFE/GNP_US_All/Polar/GNP_US_2/GNP_US") , "xvg1")
    xvg2.update_FE_data()
    xvg2.apply_correction("3D")
    xvg2.shift_zero_to_fe_plateau()

    xvg3 = generalFE("profile.xvg", Path("/media/jje63/easystore/GoldNanoparticleFE/GNP_US_All/Polar/GNP_US_3/GNP_US") , "xvg1")
    xvg3.update_FE_data()
    xvg3.apply_correction("3D")
    xvg3.shift_zero_to_fe_plateau()

    xvg4 = generalFE("profile.xvg", Path("/media/jje63/easystore/GoldNanoparticleFE/GNP_US_All/Hydrophobic/GNP_US_hyd") , "xvg1")
    xvg4.update_FE_data()
    xvg4.apply_correction("3D")
    xvg4.shift_zero_to_fe_plateau()

    xvg5 = generalFE("profile.xvg", Path("/media/jje63/easystore/GoldNanoparticleFE/GNP_US_All/Hydrophobic/GNP_US_hyd_2/GNP_US_hyd") , "xvg1")
    xvg5.update_FE_data()
    xvg5.apply_correction("3D")
    xvg5.shift_zero_to_fe_plateau()

    xvg6 = generalFE("profile.xvg", Path("/media/jje63/easystore/GoldNanoparticleFE/GNP_US_All/Hydrophobic/GNP_US_hyd_3/GNP_US_hyd") , "xvg1")
    xvg6.update_FE_data()
    xvg6.apply_correction("3D")
    xvg6.shift_zero_to_fe_plateau()


    dfstack = np.stack((np.array(xvg1.fe_data_frame["Values"][:-10]), np.array(xvg2.fe_data_frame["Values"][:-10]), np.array(xvg3.fe_data_frame["Values"][:-10])))
    dfmean = np.mean(dfstack, axis=0)
    dfstd = np.std(dfstack, axis=0)/np.sqrt(3)

    dfstackhyd = np.stack((np.array(xvg4.fe_data_frame["Values"][:-10]), np.array(xvg5.fe_data_frame["Values"][:-10]), np.array(xvg6.fe_data_frame["Values"][:-10])))
    dfmeanhyd = np.mean(dfstackhyd, axis=0)
    dfstdhyd = np.std(dfstackhyd, axis=0)/np.sqrt(3)

    diff = dfmeanhyd - dfmean 
    figure , axs = plt.subplots(1,2, figsize=(15,8),sharex=True)
    axs[0].plot(xvg4.fe_data_frame["CV"][:-10],
             dfmeanhyd,
             label="Hydrophobic(C5)")
    axs[0].plot(xvg1.fe_data_frame["CV"][:-10],
             dfmean,
             label="Polar(P5)")

    axs[0].fill_between(xvg4.fe_data_frame["CV"][:-10],
                    dfmeanhyd-dfstdhyd,
                    dfmeanhyd+dfstdhyd,
                    alpha=0.5)
    axs[0].fill_between(xvg1.fe_data_frame["CV"][:-10],
                    dfmean-dfstd,
                    dfmean+dfstd,
                    alpha=0.5)

    axs[1].plot(xvg4.fe_data_frame["CV"][:-10],
            diff,
            color='grey',
            linewidth=3)
    axs[0].axhline(y = 0, color="black", linestyle = ':')
    axs[0].set_ylabel("PMF (kJ $mol^{-1}$)", fontsize=10)
    axs[0].set_xlabel("r (nm)", fontsize=10)
    axs[0].set_yticks(np.arange(15, -115, step=20))
    axs[0].set_xticks(np.arange(2, 12, step=2))
    axs[0].legend(loc="upper right")

    axs[1].set_yticks(np.arange(-30, 30, step=10))
    axs[1].axhline(y = 0, color="black", linestyle = ':')
    axs[1].set_ylabel(r'$\Delta PMF$ ' "(kJ $mol^{-1}$)", fontsize=10)
    axs[1].set_xlabel("r (nm)", fontsize=10)
    axs[1].set_xticks(np.arange(2, 12, step=2))

    plt.savefig(Path("/media/jje63/easystore/GoldNanoparticleFE/GNP_US_All/PMF_full.pdf"),format='pdf',dpi=500, bbox_inches='tight')