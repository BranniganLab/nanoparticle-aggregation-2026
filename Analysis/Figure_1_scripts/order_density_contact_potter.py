#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 11:06:01 2023

@author: jje63
"""
import argparse
from pathlib import Path, PurePath

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

CORETYPES = ["C1","C5","N0","P1","P5",]
THIOL = ["Octanethiol","Dodecanethiol","Hexadecanethiol","Icosanethiol","Tetracosanethiol"]
REPLICA = ["Replica1","Replica2","Replica3"]
LENGTHS = [2,3,4,5,6]
DATA_FILE="tailcont"+".dat"
DATA_FILE2 = "lipidorder"+".dat"

class generalFileParse:
    def __init__(self, file_name, directory_path, data_name, data_type):
        self.directory_path = directory_path
        self.file_path = directory_path.joinpath(file_name)
        self.data_frame = pd.DataFrame()
        self.data_name = data_name
        self.data_average = None
        self.data_type = data_type
        
    def update_data(self):
        if self.file_path.exists() and self.data_type=="contact":
            data = np.loadtxt(self.file_path, comments=["#","@"])
            self.data_frame["Values"] = data[:,1]
            self.data_frame['CV'] = data[:,0]
        elif self.file_path.exists() and self.data_type=="order":
            data = np.loadtxt(self.file_path, comments=["#","@"])
            self.data_frame["Values"] = data[:,2]
            self.data_frame["Bin 1"] = data[:,1]
            self.data_frame['Bin 2'] = data[:,0]
        else:
            raise ValueError("File doesn't exist")
    
    def update_average(self, cutoff=100):
        self.data_average = self.data_frame["Values"][cutoff:].mean()
    
def make_thiol_dataset_O_C(directory_path, coretype, thiol, replica, dataname, datatype):
    paths = coretype+"/"+thiol+"/"+replica+"/analysis"
    allfilepaths = list(directory_path.resolve().glob(paths))
    LigandData = {}
    for path in allfilepaths:
        name = path.parts[-3]
        rep = path.parts[-2]
        data = generalFileParse(dataname, path, name, datatype)
        data.update_data()
        data.update_average()
        LigandData[name+"_"+rep] = data
    return LigandData

def calculate_average_std(data_set:[list]):
    npdata = np.array(data_set)
    average = np.mean(npdata)
    standard_error = np.std(npdata, ddof=1)/np.sqrt(len(data_set))
    return [average, standard_error]

def calculate_average_std_along_axis(data_set:[list]):
    average = np.mean(data_set, axis=0)
    standard_error = np.std(data_set, ddof=1,axis=0)/np.sqrt(len(data_set))
    return [average, standard_error]

def create_contact_core_replica_data(cont_rep, Thiols=THIOL, Replica_num=3):
    Coredict = pd.DataFrame()
    for thiol in Thiols:
        temp_rep = []
        for i in range(Replica_num):
            if i+1 != 3:
                temp_rep.append(cont_rep[thiol+"_"+"Replica"+str(i+1)].data_average)
            else:
                temp_rep.append(cont_rep[thiol+"_"+"Replica"+str(i+1)].data_average)
                Coredict[thiol]=calculate_average_std(temp_rep)
    return Coredict

def create_contact_full_replica_data(cont_rep, Thiols=THIOL, Replica_num=3):
    Coredict = pd.DataFrame()
    for thiol in Thiols:
        temp_rep = []
    for i in range(Replica_num):
        temp_rep = []
        for thiol in Thiols:
            temp_rep.extend(cont_rep[thiol+"_"+"Replica"+str(i+1)].data_frame["Values"].tolist())
        Coredict["Replica"+str(i)]=calculate_average_std(temp_rep)
    return Coredict

def create_order_full_replica_data(cont_rep, Thiols=THIOL, Replica_num=3):
    Coredict = pd.DataFrame()
    for thiol in Thiols:
        temp_rep = []
        for i in range(Replica_num):
            if i+1 != 3:
                temp_rep.append(np.array(cont_rep[thiol+"_"+"Replica"+str(i+1)].data_frame["Values"][0:10]))
            else:
                temp_rep.append(np.array(cont_rep[thiol+"_"+"Replica"+str(i+1)].data_frame["Values"][0:10]))
                Coredict[thiol]=calculate_average_std_along_axis(temp_rep)
    return Coredict

if __name__ == '__main__':
    DIRECTORY_PATH = Path("/media/jje63/easystore/Single_NP/")
    font = {'family': 'serif',
            'color':  'black',
            'weight': 'normal',
            'size': 25,
            }
    C1datacont = make_thiol_dataset(DIRECTORY_PATH, "C1", "*thiol", "Replica*",DATA_FILE,"contact")
    C1_replica_combined = create_contact_core_replica_data(C1datacont)
    C1_full_replica = create_contact_full_replica_data(C1datacont)
    C1AVG = C1_full_replica.mean(axis=1).iloc[0]
    C1STD = C1_full_replica.std(axis=1).iloc[0]/np.sqrt(len(C1_full_replica.columns))

    C1dataord = make_thiol_dataset(DIRECTORY_PATH, "C1", "*thiol", "Replica*",DATA_FILE2,"order")
    C1order_full_replica = create_order_full_replica_data(C1dataord)

    C5datacont = make_thiol_dataset(DIRECTORY_PATH, "C5", "*thiol", "Replica*",DATA_FILE,"contact")
    C5dataord = make_thiol_dataset(DIRECTORY_PATH, "C5", "*thiol", "Replica*",DATA_FILE2,"order")
    C5_replica_combined = create_contact_core_replica_data(C5datacont)
    C5_full_replica = create_contact_full_replica_data(C5datacont)
    C5AVG = C5_full_replica.mean(axis=1).iloc[0]
    C5STD = C5_full_replica.std(axis=1).iloc[0]/np.sqrt(len(C5_full_replica.columns)) 

    N0datacont = make_thiol_dataset(DIRECTORY_PATH, "N0", "*thiol", "Replica*",DATA_FILE,"contact")
    N0dataord = make_thiol_dataset(DIRECTORY_PATH, "N0", "*thiol", "Replica*",DATA_FILE2,"order")
    N0_replica_combined = create_contact_core_replica_data(N0datacont)
    N0_full_replica = create_contact_full_replica_data(N0datacont)
    N0AVG = N0_full_replica.mean(axis=1).iloc[0]
    N0STD = N0_full_replica.std(axis=1).iloc[0]/np.sqrt(len(N0_full_replica.columns))

    P1datacont = make_thiol_dataset(DIRECTORY_PATH, "P1", "*thiol", "Replica*",DATA_FILE,"contact")
    P1dataord = make_thiol_dataset(DIRECTORY_PATH, "P1", "*thiol", "Replica*",DATA_FILE2,"order")
    P1_replica_combined = create_contact_core_replica_data(P1datacont)
    P1_full_replica = create_contact_full_replica_data(P1datacont)
    P1AVG = P1_full_replica.mean(axis=1).iloc[0]
    P1STD = P1_full_replica.std(axis=1).iloc[0]/np.sqrt(len(P1_full_replica.columns)) 

    P5datacont = make_thiol_dataset(DIRECTORY_PATH, "P5", "*thiol", "Replica*",DATA_FILE,"contact")
    P5dataord = make_thiol_dataset(DIRECTORY_PATH, "P5", "*thiol", "Replica*",DATA_FILE2,"order")
    P5_replica_combined = create_contact_core_replica_data(P5datacont)
    P5_full_replica = create_contact_full_replica_data(P5datacont)
    P5AVG = P5_full_replica.mean(axis=1).iloc[0]
    P5STD = P5_full_replica.std(axis=1).iloc[0]/np.sqrt(len(P5_full_replica.columns)) 

    #Qadatacont = make_thiol_dataset(DIRECTORY_PATH, "Qa", "*thiol", "Replica*",DATA_FILE,"contact")
    #Qadataord = make_thiol_dataset(DIRECTORY_PATH, "Qa", "*thiol", "Replica*",DATA_FILE2,"order")
    #Qa_replica_combined = create_contact_core_replica_data(Qadatacont)
    #Qa_full_replica = create_contact_full_replica_data(Qadatacont)
    #QaAVG = Qa_full_replica.mean(axis=1).iloc[0]
    #QaSTD = Qa_full_replica.std(axis=1).iloc[0]/np.sqrt(len(Qa_full_replica.columns))

    SSdatacont = make_thiol_dataset(DIRECTORY_PATH, "SS", "*thiol", "Replica*",DATA_FILE,"contact")
    SSdataord = make_thiol_dataset(DIRECTORY_PATH, "SS", "*thiol", "Replica*",DATA_FILE2,"order")
    SS_replica_combined = create_contact_core_replica_data(SSdatacont)
    SS_full_replica = create_contact_full_replica_data(SSdatacont)
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

    for i,thiol in enumerate(THIOL):
        coreplot = [Cores[0][thiol].iloc[0],
                    Cores[1][thiol].iloc[0],
                    Cores[2][thiol].iloc[0],
                    Cores[3][thiol].iloc[0],
                    Cores[4][thiol].iloc[0],
                    #Cores[5][thiol].iloc[0],
                    #Cores[6][thiol].iloc[0]
                ]
        Divide = max(coreplot)
        coreplotstd = [Cores[0][thiol].iloc[1],
                    Cores[1][thiol].iloc[1],
                    Cores[2][thiol].iloc[1],
                    Cores[3][thiol].iloc[1],
                    Cores[4][thiol].iloc[1],
                    #Cores[5][thiol].iloc[1],
                    #Cores[6][thiol].iloc[1]
                    ]
        axs.errorbar( CORETYPES
                        ,coreplot
                        ,yerr=coreplotstd/np.sqrt(3)
                        ,capsize=4
                        ,fmt='-o'
                        ,label=thiol
            )
        axs.errorbar( "SS"
                    ,Cores[5][thiol].iloc[0]
                    ,yerr=Cores[5][thiol].iloc[1]
                    ,fmt='-o'
                        )
    axs.set_xlabel("Core Parameter", fontdict=font)
    axs.set_ylabel(r"Average Contacts", fontdict=font)
    axs.legend()
    axs.tick_params(axis='both', labelsize=20)
    figure.savefig(DIRECTORY_PATH.joinpath("LipidTailGroupDistrib.pdf"),format='pdf',dpi=500, bbox_inches='tight')

    figure2 , axs2 = plt.subplots(1, figsize=(10,8))
    axs2.errorbar(CORETYPES
                ,[C1AVG,C5AVG,N0AVG,P1AVG,P5AVG]
                ,yerr=[C1STD,C5STD,N0STD,P1STD,P5STD]
                ,fmt='-o'
                ,capsize=12
                ,elinewidth=3
                ,capthick=3
                ,color="black"
                ,linewidth=3
                ,markersize=12)
    axs2.errorbar( "SS"
                ,SSAVG
                ,yerr=SSSTD
                ,fmt='-o'
                ,capsize=12
                ,elinewidth=3
                ,capthick=3
                ,color="Orange"
                ,markersize=12
                )
    axs2.set_xlabel("Core Parameter", fontdict=font)
    axs2.set_ylabel(r"Average Contacts", fontdict=font)
    axs2.tick_params(axis='both', labelsize=20)
    figure2.savefig(DIRECTORY_PATH.joinpath("LipidTailGroupDistrib_full.pdf"),format='pdf',dpi=500, bbox_inches='tight')

    #figure3, axs3 = plt.subplots(1, figsize=(10,6))
    #axs3.errorbar( C1dataord["Tetracosanethiol_Replica1"].data_frame["Bin 1"][0:10]
    #              ,C1order_full_replica["Tetracosanethiol"].iloc[0]
    #    )