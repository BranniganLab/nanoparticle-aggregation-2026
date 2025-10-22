#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 17:25:25 2025

@author: jje63
"""

import argparse
from pathlib import Path, PurePath

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

CORETYPES = ["C1","C5","N0","P1","P5"]
CORETYPES2 = ["C1","C5","N0","P1","P5","SS"]
THIOL = ["Octanethiol","Dodecanethiol","Hexadecanethiol","Icosanethiol","Tetracosanethiol"]
#REPLICA = ["Replica1","Replica2","Replica3"]
LENGTHS = [2,3,4,5,6]

class generalSASA:
    def __init__(self, file_name, directory_path, data_name):
        self.directory_path = directory_path
        self.file_path = directory_path.joinpath(file_name)
        self.sasa_data_frame = pd.DataFrame()
        self.data_name = data_name
        self.data_average = None
        
    def update_SASA_data(self, cutoff=200):
        if self.file_path.exists():
            SASA_data = np.loadtxt(self.file_path, comments=["#","@"])
            self.sasa_data_frame["Values"] = SASA_data[cutoff:,1]
            self.sasa_data_frame['CV'] = SASA_data[cutoff:,0]
        else:
            raise ValueError("File doesn't exist")
            
    def update_SASA_average(self):
        self.data_average = self.sasa_data_frame["Values"].mean()
        

def make_thiol_dataset(directory_path, coretype, thiol, replica, dataname):
    paths = coretype+"/"+thiol+"/"+replica+"/analysis"
    
    allfilepaths = list(directory_path.resolve().glob(paths))
    LigandData = {}
    for path in allfilepaths:
        name = path.parts[-3]
        rep = path.parts[-2]
        data = generalSASA(dataname, path, name)
        data.update_SASA_data()
        data.update_SASA_average()
        LigandData[name+"_"+rep] = data
    return LigandData

def calculate_average_std(data_set:[list]):
    npdata = np.array(data_set)
    average = np.mean(npdata)
    standard_error = np.std(npdata, ddof=1)/np.sqrt(len(data_set))
    return [average, standard_error]

def create_sasa_core_replica_data(SASA_rep, Thiols=THIOL, Replica_num=3):
    Coredict = pd.DataFrame()
    for thiol in Thiols:
        temp_rep = []
        for i in range(Replica_num):
            if i+1 != 3:
                temp_rep.append(SASA_rep[thiol+"_"+"Replica"+str(i+1)].data_average)
            else:
                temp_rep.append(SASA_rep[thiol+"_"+"Replica"+str(i+1)].data_average)
                Coredict[thiol]=calculate_average_std(temp_rep)
    return Coredict

def create_sasa_full_replica_data(SASA_rep, Thiols=THIOL, Replica_num=3):
    Coredict = pd.DataFrame()
    for thiol in Thiols:
        temp_rep = []
    for i in range(Replica_num):
        temp_rep = []
        for thiol in Thiols:
            temp_rep.extend(SASA_rep[thiol+"_"+"Replica"+str(i+1)].sasa_data_frame["Values"].tolist())
        Coredict["Replica"+str(i)]=calculate_average_std(temp_rep)
    return Coredict
    

if __name__ == '__main__':
    DIRECTORY_PATH = Path("/media/jje63/easystore/Single_NP/")
    CORETYPES = ["C1","C5","N0","P1","P5"]
    CORETYPES2 = ["C1","C5","N0","P1","P5","SS"]
    THIOL = ["Octanethiol","Dodecanethiol","Hexadecanethiol","Icosanethiol","Tetracosanethiol"]
    #REPLICA = ["Replica1","Replica2","Replica3"]
    LENGTHS = [2,3,4,5,6]
    DATA_FILE="watersasa"+".dat"
    font = {'family': 'serif',
            'color':  'black',
            'weight': 'normal',
            'size': 25,
            }
    C1data = make_thiol_dataset(DIRECTORY_PATH, "C1", "*thiol", "Replica*",DATA_FILE)
    C1_replica_combined = create_sasa_core_replica_data(C1data)
    C1_full_replica = create_sasa_full_replica_data(C1data)
    C1AVG = C1_full_replica.mean(axis=1).iloc[0]
    C1STD = C1_full_replica.std(axis=1).iloc[0]/np.sqrt(len(C1_full_replica.columns)) 

    C5data = make_thiol_dataset(DIRECTORY_PATH, "C5", "*thiol", "Replica*",DATA_FILE)
    C5_replica_combined = create_sasa_core_replica_data(C5data)
    C5_full_replica = create_sasa_full_replica_data(C5data)
    C5AVG = C5_full_replica.mean(axis=1).iloc[0]
    C5STD = C5_full_replica.std(axis=1).iloc[0]/np.sqrt(len(C5_full_replica.columns)) 

    N0data = make_thiol_dataset(DIRECTORY_PATH, "N0", "*thiol", "Replica*",DATA_FILE)
    N0_replica_combined = create_sasa_core_replica_data(N0data)
    N0_full_replica = create_sasa_full_replica_data(N0data)
    N0AVG = N0_full_replica.mean(axis=1).iloc[0]
    N0STD = N0_full_replica.std(axis=1).iloc[0]/np.sqrt(len(N0_full_replica.columns)) 
    
    P1data = make_thiol_dataset(DIRECTORY_PATH, "P1", "*thiol", "Replica*",DATA_FILE)
    P1_replica_combined = create_sasa_core_replica_data(P1data)
    P1_full_replica = create_sasa_full_replica_data(P1data)
    P1AVG = P1_full_replica.mean(axis=1).iloc[0]
    P1STD = P1_full_replica.std(axis=1).iloc[0]/np.sqrt(len(P1_full_replica.columns)) 
    
    P5data = make_thiol_dataset(DIRECTORY_PATH, "P5", "*thiol", "Replica*",DATA_FILE)
    P5_replica_combined = create_sasa_core_replica_data(P5data)
    P5_full_replica = create_sasa_full_replica_data(P5data)
    P5AVG = P5_full_replica.mean(axis=1).iloc[0]
    P5STD = P5_full_replica.std(axis=1).iloc[0]/np.sqrt(len(P5_full_replica.columns)) 
    
    #Qadata = make_thiol_dataset(DIRECTORY_PATH, "Qa", "*thiol", "Replica*",DATA_FILE)
    #Qa_replica_combined = create_sasa_core_replica_data(Qadata)
    #Qa_full_replica = create_sasa_full_replica_data(Qadata)
    #QaAVG = Qa_full_replica.mean(axis=1).iloc[0]
    #QaSTD = Qa_full_replica.std(axis=1).iloc[0]/np.sqrt(len(Qa_full_replica.columns)) 
    
    
    SSdata = make_thiol_dataset(DIRECTORY_PATH, "SS", "*thiol", "Replica*",DATA_FILE)
    SS_replica_combined = create_sasa_core_replica_data(SSdata)
    SS_full_replica = create_sasa_full_replica_data(SSdata)
    SSAVG = SS_full_replica.mean(axis=1).iloc[0]
    SSSTD = SS_full_replica.std(axis=1).iloc[0]/np.sqrt(len(SS_full_replica.columns))
    
    Cores = [ C1_replica_combined
             ,C5_replica_combined
             ,N0_replica_combined
             ,P1_replica_combined
             ,P5_replica_combined
             #,Qa_replica_combined
             ,SS_replica_combined]
    
    figure , axs = plt.subplots(1, figsize=(10,8))
    for i,core in enumerate(Cores):
        Data = [ core[THIOL[0]].iloc[0] 
                ,core[THIOL[1]].iloc[0] 
                ,core[THIOL[2]].iloc[0] 
                ,core[THIOL[3]].iloc[0]
                ,core[THIOL[4]].iloc[0]
                ]
        STDData = [ core[THIOL[0]].iloc[1] 
                   ,core[THIOL[1]].iloc[1] 
                   ,core[THIOL[2]].iloc[1] 
                   ,core[THIOL[3]].iloc[1]
                   ,core[THIOL[4]].iloc[1]
                  ]
        axs.errorbar(LENGTHS
                    ,Data 
                    ,yerr=STDData
                    ,capsize=12
                    ,elinewidth=3
                    ,capthick=3
                    ,fmt='-o'
                    ,label=CORETYPES2[i]
                    ,linewidth=3
                    ,markersize=12)
    axs.set_xticks(LENGTHS, fontdict=font)
    axs.set_xlabel("Ligand Length", fontdict=font)
    axs.set_ylabel(r"Water SASA (nm$^{2}$)", fontdict=font)
    axs.tick_params(axis='both', labelsize=20)
    axs.legend(fontsize=20, bbox_to_anchor=(1.02, 1.46))
    figure.savefig(DIRECTORY_PATH.joinpath("WaterSASAplot_length.pdf"),format='pdf',dpi=500, bbox_inches='tight')
    
    figure3 , axs3 = plt.subplots(1, figsize=(10,8))
    for i,thiol in enumerate(THIOL):
        coreplot = [Cores[0][thiol].iloc[0],
                    Cores[1][thiol].iloc[0],
                    Cores[2][thiol].iloc[0],
                    Cores[3][thiol].iloc[0],
                    Cores[4][thiol].iloc[0],
                    Cores[5][thiol].iloc[0],
                    #Cores[6][thiol].iloc[0]
                    ]
        coreplotstd = [Cores[0][thiol].iloc[1],
                    Cores[1][thiol].iloc[1],
                    Cores[2][thiol].iloc[1],
                    Cores[3][thiol].iloc[1],
                    Cores[4][thiol].iloc[1],
                    Cores[5][thiol].iloc[1],
                    #Cores[6][thiol].iloc[1]
                    ]
        axs3.errorbar( CORETYPES2
                        ,coreplot
                        ,yerr=coreplotstd
                        ,capsize=12
                        ,elinewidth=3
                        ,capthick=3
                        ,fmt='-o'
                        ,label=thiol
                        ,linewidth=3
                        ,markersize=12
            )
        
    axs3.set_xlabel("Core Parameter", fontdict=font)
    axs3.set_ylabel(r"Water SASA (nm$^{2}$)", fontdict=font)
    axs3.legend(fontsize=20, bbox_to_anchor=(1.02, 1.38))
    axs3.tick_params(axis='both', labelsize=20)
    figure3.savefig(DIRECTORY_PATH.joinpath("WaterSASAplot_core.pdf"),format='pdf',dpi=500, bbox_inches='tight')
    
    figure2 , axs2 = plt.subplots(1, figsize=(8,6))
    axs2.errorbar(CORETYPES
                   ,[C1AVG,C5AVG,N0AVG,P1AVG,P5AVG]
                   ,yerr=[C1STD,C5STD,N0STD,P1STD,P5STD]
                   ,fmt='-o'
                   ,capsize=12
                   ,elinewidth=3
                   ,color="black"
                   ,linewidth=3
                   ,markersize=12)
    axs2.errorbar("SS"
                   ,SSAVG
                   ,yerr=SSSTD
                   ,fmt='-o'
                   ,capsize=12
                   ,elinewidth=3
                   ,capthick=3
                   ,color="Orange"
                   ,linewidth=3
                   ,markersize=12
                   )
    axs2.set_xlabel("Core Parameter", fontdict=font)
    axs2.set_ylabel(r"Water SASA (nm$^{2}$)", fontdict=font)
    axs2.tick_params(axis='both', labelsize=20)
    figure2.savefig(DIRECTORY_PATH.joinpath("Watercoreplot.pdf"),format='pdf',dpi=500, bbox_inches='tight')
   


