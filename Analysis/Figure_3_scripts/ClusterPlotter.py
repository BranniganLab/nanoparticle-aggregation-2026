#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 12:07:10 2025

@author: jje63
"""

import argparse
from pathlib import Path, PurePath
import re

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def convert_string_to_num(NumberString):
    StringList = NumberString.split()
    NumList = [eval(i) for i in StringList]
    return NumList

def remove_zeros_from_list_of_lists(list_of_lists):
    return [[element for element in sublist if element != 0] for sublist in list_of_lists]

def find_max_list(lists):
    index = 0
    listlen = 0
    longest_list = lists[index]
    for i in range(len(lists)):
        if len(lists[i]) > listlen:
            listlen = len(lists[i])
            longest_list = lists[i]
            index = i        
    return longest_list

font2 = {'family':'serif',
        'weight':'normal',
        'size': 12,
        }


class generalCluster:
    
    def __init__(self, filepath, agg_size=10):
        self.filepath = filepath
        cluster_info = self.parse_cluster_information()
        self.frame_data = cluster_info[0]
        self.frame_over_time = np.array(cluster_info[1])
        self.largest_aggregate_fraction_over_time = np.array(cluster_info[2])
        self.monomer_fraction_over_time = np.array(cluster_info[3])
        self.average_largest_aggregate_fraction = np.mean(np.array(cluster_info[5]))/agg_size
        self.average_monomer_fraction = np.mean(np.array(cluster_info[4]))/agg_size
        
        
    
    def parse_cluster_information(self, agg_size=10):
        ClusterFilePath = open(self.filepath)
        largest_aggregate_fraction_over_time = []
        monomer_fraction_over_time = []
        frame_over_time = []
        monomers_full = []
        la_full = []
        frame_info_dict = {}
        for clusterdata in ClusterFilePath:
            clframe = int(clusterdata.split()[0])
            if clusterdata.split()[1].isdigit():
                sclus = clusterdata.split()
                sclus[1] = "{"+clusterdata.split()[1]+"}"
                clusterdata = ' '.join(sclus)
            clusters = re.findall("\\{.*\\}", clusterdata)[0].split("} {")
            full_clusters=[convert_string_to_num(cluster.replace("{","").replace("}","")) for cluster in clusters]
            aggregates = remove_zeros_from_list_of_lists(full_clusters[1:])
            if "{" in clusterdata.split()[1]:
                monomers = np.array(full_clusters[0])
            else:
                monomers = [int(clusterdata.split()[1])]
            monomers_full.append(len(monomers))
            if aggregates != [] and aggregates[0] != []:
                largest_aggregate = np.array(find_max_list(aggregates))
                dev_len = len(full_clusters[1])
            else:
                largest_aggregate = np.array([0])
                dev_len = 1
            all_aggregate_sizes = [len(aggregate) for aggregate in aggregates]
            aggregate_dict = {
                 "monomers" : monomers
                ,"aggregates" : aggregates
                ,"monomer fraction" : len(monomers)/agg_size
                ,"largest aggregate fraction" : len(largest_aggregate)/agg_size
                ,"all aggregate sizes" : all_aggregate_sizes
                }
            largest_aggregate_fraction_over_time.append(len(largest_aggregate)/agg_size)
            monomer_fraction_over_time.append(len(monomers)/agg_size)
            la_full.append(len(largest_aggregate))
            frame_over_time.append(clframe)
            
            frame_info_dict[clframe] = aggregate_dict
        return [frame_info_dict, frame_over_time, largest_aggregate_fraction_over_time, monomer_fraction_over_time, monomers_full,la_full]

class multiClusterData:
    def __init__(self, filepaths:[list]):
        self.directories = filepaths
        self.all_replicas = [generalCluster(gencluster) for gencluster in self.directories] 
        all_averages = self.concatenate_averages()
        self.all_la_fraction = np.mean(all_averages[0])
        self.all_monomer_fraction = np.mean(all_averages[1])
        self.monomer_over_time = self.average_arrays(all_averages[2])
        self.la_over_time = self.average_arrays(all_averages[3])
        self.monomer_standard_error = np.std(all_averages[1])/np.sqrt(len(all_averages[1]))
        self.la_standard_error = np.std(all_averages[0])/np.sqrt(len(all_averages[0]))
        self.la_over_time_standard_error = self.std_arrays(all_averages[3])/np.sqrt(len(all_averages[0]))
        self.monomer_over_time_standard_error = self.std_arrays(all_averages[2])/np.sqrt(len(all_averages[1]))
        
    def average_arrays(self, array_list):
        stack = np.stack(array_list)
        return np.nanmean(stack, axis=0)
    
    def std_arrays(self, array_list):
        stack = np.stack(array_list)
        return np.nanstd(stack,axis=0)
    
    def concatenate_averages(self):
        average_la_array = []
        average_monomer_array = []
        monomer_over_time = []
        la_over_time = []
        monomer_time = [monotime.monomer_fraction_over_time for monotime in self.all_replicas]
        la_time = [latime.largest_aggregate_fraction_over_time for latime in self.all_replicas]
        length_mono = len(max(monomer_time, key=len))
        length_la = len(max(la_time, key=len))
        for obj in self.all_replicas:
            object_mono_length = len(obj.monomer_fraction_over_time)
            average_la_array.append(obj.average_largest_aggregate_fraction)
            average_monomer_array.append(obj.average_monomer_fraction)
            mono_time_pad = np.pad(obj.monomer_fraction_over_time, pad_width=(0, length_mono-object_mono_length), constant_values=np.nan)
            monomer_over_time.append(mono_time_pad)
            la_time_pad = np.pad(obj.largest_aggregate_fraction_over_time, pad_width=(0, length_la-object_mono_length), constant_values=np.nan)
            la_over_time.append(la_time_pad)
        return [average_la_array, average_monomer_array, monomer_over_time, la_over_time]
        
    
if __name__=="__main__":
    
    base_dir = "/media/jje63/easystore/"
    sub_dir_base = ["Common_Nanoparticle","PolarNP","Soft_Sphere" ]
    thiol_name = ["Octanethiol", "Dodecanthiol","Hexadecanethiol","Icosanethiol","Tetracosanethiol"]
    file_name = "ClusterAU10.dat"
    data_bins = [{},{},{}]
    
    for i in range(len(sub_dir_base)):
        bins = data_bins[i]
        for j in range(len(thiol_name)):
            paths = Path("/media/jje63/easystore1/").glob(sub_dir_base[i]+"*/"+thiol_name[j]+"/"+file_name)
            data = multiClusterData(paths)
            bins[thiol_name[j]] = data
    
    figure , axs = plt.subplots(1, figsize=(8,6), sharex=True)
    figure2 , axs2 = plt.subplots(1, figsize=(8,6), sharex=True)
    
    ### Monomer Over Time ###
    figure3 , axs3 = plt.subplots(1, figsize=(8,6), sharex=True)
    figure4 , axs4 = plt.subplots(1, figsize=(8,6), sharex=True)
    figure5 , axs5 = plt.subplots(1, figsize=(8,6), sharex=True)
    
    ### Largest Aggregate Over Time ###
    figure6 , axs6 = plt.subplots(1, figsize=(8,6), sharex=True)
    figure7 , axs7 = plt.subplots(1, figsize=(8,6), sharex=True)
    figure8 , axs8 = plt.subplots(1, figsize=(8,6), sharex=True)
    
    ### Monomer Fraction Plotting ###
    axs.errorbar([8,12,16,20,24],
                 [data_bins[0]["Octanethiol"].all_monomer_fraction
                 ,data_bins[0]["Dodecanthiol"].all_monomer_fraction
                 ,data_bins[0]["Hexadecanethiol"].all_monomer_fraction
                 ,data_bins[0]["Icosanethiol"].all_monomer_fraction
                 ,data_bins[0]["Tetracosanethiol"].all_monomer_fraction
                  ],
                 yerr=[data_bins[0]["Octanethiol"].monomer_standard_error
                      ,data_bins[0]["Dodecanthiol"].monomer_standard_error
                      ,data_bins[0]["Hexadecanethiol"].monomer_standard_error
                      ,data_bins[0]["Icosanethiol"].monomer_standard_error
                      ,data_bins[0]["Tetracosanethiol"].monomer_standard_error
                     ]
                ,linestyle='solid'
                ,linewidth=3
                ,marker='o'
                ,alpha=0.5
                ,markersize = 13
                ,capsize=8
                ,color="#003dfc"
                ,label="Hydrophobic"
        )
    
    
    axs.errorbar([8,12,16,20,24],
                 [data_bins[1]["Octanethiol"].all_monomer_fraction
                 ,data_bins[1]["Dodecanthiol"].all_monomer_fraction
                 ,data_bins[1]["Hexadecanethiol"].all_monomer_fraction
                 ,data_bins[1]["Icosanethiol"].all_monomer_fraction
                 ,data_bins[1]["Tetracosanethiol"].all_monomer_fraction
                  ],
                 yerr=[data_bins[1]["Octanethiol"].monomer_standard_error
                      ,data_bins[1]["Dodecanthiol"].monomer_standard_error
                      ,data_bins[1]["Hexadecanethiol"].monomer_standard_error
                      ,data_bins[1]["Icosanethiol"].monomer_standard_error
                      ,data_bins[1]["Tetracosanethiol"].monomer_standard_error
                     ]
                ,linestyle='solid'
                ,linewidth=3, marker='^'
                ,markersize = 13
                ,capsize=8
                ,color="#fc8900"
                ,label="Polar"
        )
    
    axs.errorbar([8,12,16,20,24],
                 [data_bins[2]["Octanethiol"].all_monomer_fraction
                 ,data_bins[2]["Dodecanthiol"].all_monomer_fraction
                 ,data_bins[2]["Hexadecanethiol"].all_monomer_fraction
                 ,data_bins[2]["Icosanethiol"].all_monomer_fraction
                 ,data_bins[2]["Tetracosanethiol"].all_monomer_fraction
                  ],
                 yerr=[data_bins[2]["Octanethiol"].monomer_standard_error
                      ,data_bins[2]["Dodecanthiol"].monomer_standard_error
                      ,data_bins[2]["Hexadecanethiol"].monomer_standard_error
                      ,data_bins[2]["Icosanethiol"].monomer_standard_error
                      ,data_bins[2]["Tetracosanethiol"].monomer_standard_error
                     ]
                , linestyle='solid'
                ,linewidth=3,marker='o'
                ,markersize = 13
                ,capsize=8
                ,color="grey"
                ,label="Soft Sphere"
        )
    axs.set_yticks(np.arange(0, 1.2, step=0.2))
    axs.tick_params(axis='y', labelsize=15)
    axs.tick_params(axis='x', labelsize=15)
    axs.set_yticklabels(["$0.0$","$0.2$","$0.4$","$0.6$","$0.8$","$1.0$"])
    axs.set_ylabel(r'$\langle F_{m} \rangle$',size=15)
    axs.set_xlabel('Ligand Length',size=15)
    axs.legend(loc="upper right")
    
    ### Largest Aggregate Fraction Plotting ###
    axs2.errorbar([8,12,16,20,24],
                 [data_bins[0]["Octanethiol"].all_la_fraction
                 ,data_bins[0]["Dodecanthiol"].all_la_fraction
                 ,data_bins[0]["Hexadecanethiol"].all_la_fraction
                 ,data_bins[0]["Icosanethiol"].all_la_fraction
                 ,data_bins[0]["Tetracosanethiol"].all_la_fraction
                  ],
                 yerr=[data_bins[0]["Octanethiol"].la_standard_error
                      ,data_bins[0]["Dodecanthiol"].la_standard_error
                      ,data_bins[0]["Hexadecanethiol"].la_standard_error
                      ,data_bins[0]["Icosanethiol"].la_standard_error
                      ,data_bins[0]["Tetracosanethiol"].la_standard_error
                     ]
                ,linestyle='solid'
                ,linewidth=3
                ,marker='o'
                ,alpha=0.5
                ,markersize = 13
                ,capsize=8
                ,color="#003dfc"
                ,label="Hydrophobic"
        )
    
    
    axs2.errorbar([8,12,16,20,24],
                 [data_bins[1]["Octanethiol"].all_la_fraction
                 ,data_bins[1]["Dodecanthiol"].all_la_fraction
                 ,data_bins[1]["Hexadecanethiol"].all_la_fraction
                 ,data_bins[1]["Icosanethiol"].all_la_fraction
                 ,data_bins[1]["Tetracosanethiol"].all_la_fraction
                  ],
                 yerr=[data_bins[1]["Octanethiol"].la_standard_error
                      ,data_bins[1]["Dodecanthiol"].la_standard_error
                      ,data_bins[1]["Hexadecanethiol"].la_standard_error
                      ,data_bins[1]["Icosanethiol"].la_standard_error
                      ,data_bins[1]["Tetracosanethiol"].la_standard_error
                     ]
                ,linestyle='solid'
                ,linewidth=3, marker='^'
                ,markersize = 13
                ,capsize=8
                ,color="#fc8900"
                ,label="Polar"
        )
    
    axs2.errorbar([8,12,16,20,24],
                 [data_bins[2]["Octanethiol"].all_la_fraction
                 ,data_bins[2]["Dodecanthiol"].all_la_fraction
                 ,data_bins[2]["Hexadecanethiol"].all_la_fraction
                 ,data_bins[2]["Icosanethiol"].all_la_fraction
                 ,data_bins[2]["Tetracosanethiol"].all_la_fraction
                  ],
                 yerr=[data_bins[2]["Octanethiol"].la_standard_error
                      ,data_bins[2]["Dodecanthiol"].la_standard_error
                      ,data_bins[2]["Hexadecanethiol"].la_standard_error
                      ,data_bins[2]["Icosanethiol"].la_standard_error
                      ,data_bins[2]["Tetracosanethiol"].la_standard_error
                     ]
                , linestyle='solid'
                ,linewidth=3,marker='o'
                ,markersize = 13
                ,capsize=8
                ,color="grey"
                ,label="Soft Sphere"
        )
    axs2.set_yticks(np.arange(0, 1.2, step=0.2))
    axs2.tick_params(axis='y', labelsize=15)
    axs2.tick_params(axis='x', labelsize=15)
    axs2.set_yticklabels(["$0.0$","$0.2$","$0.4$","$0.6$","$0.8$","$1.0$"])
    axs2.set_ylabel(r'$\langle F_{a} \rangle$',size=15)
    axs2.set_xlabel('Ligand Length',size=15)
    axs2.legend(loc="upper right")
    
    ### Monomer Over Time Hydrophobic ####
    axs3.errorbar(data_bins[0]["Octanethiol"].all_replicas[0].frame_over_time/100-2.5
                 ,data_bins[0]["Octanethiol"].monomer_over_time
                 ,yerr = data_bins[0]["Octanethiol"].monomer_over_time_standard_error
                 ,label = "Octanethiol"
        )
    axs3.errorbar(data_bins[0]["Dodecanthiol"].all_replicas[1].frame_over_time/100-2.5
                 ,data_bins[0]["Dodecanthiol"].monomer_over_time
                 ,yerr = data_bins[0]["Dodecanthiol"].monomer_over_time_standard_error
                 ,label = "Dodecanthiol"
        )
    axs3.errorbar(data_bins[0]["Hexadecanethiol"].all_replicas[0].frame_over_time/100-2.5
                 ,data_bins[0]["Hexadecanethiol"].monomer_over_time
                 ,yerr = data_bins[0]["Hexadecanethiol"].monomer_over_time_standard_error
                 ,label = "Hexadecanethiol"
        )
    axs3.errorbar(data_bins[0]["Icosanethiol"].all_replicas[0].frame_over_time/100-2.5
                 ,data_bins[0]["Icosanethiol"].monomer_over_time
                 ,yerr = data_bins[0]["Icosanethiol"].monomer_over_time_standard_error
                 ,label = "Icosanethiol"
        )
    axs3.errorbar(data_bins[0]["Tetracosanethiol"].all_replicas[0].frame_over_time/100-2.5
                 ,data_bins[0]["Tetracosanethiol"].monomer_over_time
                 ,yerr = data_bins[0]["Tetracosanethiol"].monomer_over_time_standard_error
                 ,label = "Tetracosanethiol"
        )
    
    axs3.set_yticks(np.arange(0, 1.2, step=0.2))
    axs3.tick_params(axis='y', labelsize=15)
    axs3.tick_params(axis='x', labelsize=15)
    axs3.set_ylabel(r'$\langle F_{m} \rangle$',size=15)
    axs3.set_xlabel(r'Time $\mu s$',size=15)
    axs3.legend()
    
    ### Monomer Over Time Polar ####
    axs4.errorbar(data_bins[1]["Octanethiol"].all_replicas[0].frame_over_time/100-2.5
                 ,data_bins[1]["Octanethiol"].monomer_over_time
                 ,yerr = data_bins[1]["Octanethiol"].monomer_over_time_standard_error
                 ,label = "Octanethiol"
        )
    axs4.errorbar(data_bins[1]["Dodecanthiol"].all_replicas[1].frame_over_time/100-2.5
                 ,data_bins[1]["Dodecanthiol"].monomer_over_time
                 ,yerr = data_bins[1]["Dodecanthiol"].monomer_over_time_standard_error
                 ,label = "Dodecanthiol"
        )
    axs4.errorbar(data_bins[1]["Hexadecanethiol"].all_replicas[0].frame_over_time/100-2.5
                 ,data_bins[1]["Hexadecanethiol"].monomer_over_time
                 ,yerr = data_bins[1]["Hexadecanethiol"].monomer_over_time_standard_error
                 ,label = "Hexadecanethiol"
        )
    axs4.errorbar(data_bins[1]["Icosanethiol"].all_replicas[0].frame_over_time/100-2.5
                 ,data_bins[1]["Icosanethiol"].monomer_over_time
                 ,yerr = data_bins[1]["Icosanethiol"].monomer_over_time_standard_error
                 ,label = "Icosanethiol"
        )
    axs4.errorbar(data_bins[1]["Tetracosanethiol"].all_replicas[0].frame_over_time/100-2.5
                 ,data_bins[1]["Tetracosanethiol"].monomer_over_time
                 ,yerr = data_bins[1]["Tetracosanethiol"].monomer_over_time_standard_error
                 ,label = "Tetracosanethiol"
        )
    
    axs4.set_yticks(np.arange(0, 1.2, step=0.2))
    axs4.tick_params(axis='y', labelsize=15)
    axs4.tick_params(axis='x', labelsize=15)
    axs4.set_ylabel(r'$\langle F_{m} \rangle$',size=15)
    axs4.set_xlabel(r'Time $\mu s$',size=15)
    axs4.legend()
    
    ### Monomer Over Time Soft Sphere ####
    axs5.errorbar(data_bins[2]["Octanethiol"].all_replicas[0].frame_over_time/100-2.5
                 ,data_bins[2]["Octanethiol"].monomer_over_time
                 ,yerr = data_bins[2]["Octanethiol"].monomer_over_time_standard_error
                 ,label = "Octanethiol"
        )
    axs5.errorbar(data_bins[2]["Dodecanthiol"].all_replicas[1].frame_over_time/100-2.5
                 ,data_bins[2]["Dodecanthiol"].monomer_over_time
                 ,yerr = data_bins[2]["Dodecanthiol"].monomer_over_time_standard_error
                 ,label = "Dodecanthiol"
        )
    axs5.errorbar(data_bins[2]["Hexadecanethiol"].all_replicas[0].frame_over_time/100-2.5
                 ,data_bins[2]["Hexadecanethiol"].monomer_over_time
                 ,yerr = data_bins[2]["Hexadecanethiol"].monomer_over_time_standard_error
                 ,label = "Hexadecanethiol"
        )
    axs5.errorbar(data_bins[2]["Icosanethiol"].all_replicas[0].frame_over_time/100-2.5
                 ,data_bins[2]["Icosanethiol"].monomer_over_time
                 ,yerr = data_bins[2]["Icosanethiol"].monomer_over_time_standard_error
                 ,label = "Icosanethiol"
        )
    axs5.errorbar(data_bins[2]["Tetracosanethiol"].all_replicas[0].frame_over_time/100-2.5
                 ,data_bins[2]["Tetracosanethiol"].monomer_over_time
                 ,yerr = data_bins[2]["Tetracosanethiol"].monomer_over_time_standard_error
                 ,label = "Tetracosanethiol"
        )
    
    axs5.set_yticks(np.arange(0, 1.2, step=0.2))
    axs5.tick_params(axis='y', labelsize=15)
    axs5.tick_params(axis='x', labelsize=15)
    axs5.set_ylabel(r'$\langle F_{m} \rangle$',size=15)
    axs5.set_xlabel(r'Time $\mu s$',size=15)
    axs5.legend()
    
    ### Largest Aggregate Over Time Hydrophobic ####
    axs6.errorbar(data_bins[0]["Octanethiol"].all_replicas[0].frame_over_time/100-2.5
                 ,data_bins[0]["Octanethiol"].la_over_time
                 ,yerr = data_bins[0]["Octanethiol"].la_over_time_standard_error
                 ,label = "Octanethiol"
        )
    axs6.errorbar(data_bins[0]["Dodecanthiol"].all_replicas[1].frame_over_time/100-2.5
                 ,data_bins[0]["Dodecanthiol"].la_over_time
                 ,yerr = data_bins[0]["Dodecanthiol"].la_over_time_standard_error
                 ,label = "Dodecanthiol"
        )
    axs6.errorbar(data_bins[0]["Hexadecanethiol"].all_replicas[0].frame_over_time/100-2.5
                 ,data_bins[0]["Hexadecanethiol"].la_over_time
                 ,yerr = data_bins[0]["Hexadecanethiol"].la_over_time_standard_error
                 ,label = "Hexadecanethiol"
        )
    axs6.errorbar(data_bins[0]["Icosanethiol"].all_replicas[0].frame_over_time/100-2.5
                 ,data_bins[0]["Icosanethiol"].la_over_time
                 ,yerr = data_bins[0]["Icosanethiol"].la_over_time_standard_error
                 ,label = "Icosanethiol"
        )
    axs6.errorbar(data_bins[0]["Tetracosanethiol"].all_replicas[0].frame_over_time/100-2.5
                 ,data_bins[0]["Tetracosanethiol"].la_over_time
                 ,yerr = data_bins[0]["Tetracosanethiol"].la_over_time_standard_error
                 ,label = "Tetracosanethiol"
        )
    
    axs6.set_yticks(np.arange(0, 1.2, step=0.2))
    axs6.tick_params(axis='y', labelsize=15)
    axs6.tick_params(axis='x', labelsize=15)
    axs6.set_ylabel(r'$\langle F_{a} \rangle$',size=15)
    axs6.set_xlabel(r'Time $\mu s$',size=15)
    axs6.legend()
    
    ### Largest Aggregate Over Time Polar ####
    axs7.errorbar(data_bins[1]["Octanethiol"].all_replicas[0].frame_over_time/100-2.5
                 ,data_bins[1]["Octanethiol"].la_over_time
                 ,yerr = data_bins[1]["Octanethiol"].la_over_time_standard_error
                 ,label = "Octanethiol"
        )
    axs7.errorbar(data_bins[1]["Dodecanthiol"].all_replicas[1].frame_over_time/100-2.5
                 ,data_bins[1]["Dodecanthiol"].la_over_time
                 ,yerr = data_bins[1]["Dodecanthiol"].la_over_time_standard_error
                 ,label = "Dodecanthiol"
        )
    axs7.errorbar(data_bins[1]["Hexadecanethiol"].all_replicas[0].frame_over_time/100-2.5
                 ,data_bins[1]["Hexadecanethiol"].la_over_time
                 ,yerr = data_bins[1]["Hexadecanethiol"].la_over_time_standard_error
                 ,label = "Hexadecanethiol"
        )
    axs7.errorbar(data_bins[1]["Icosanethiol"].all_replicas[0].frame_over_time/100-2.5
                 ,data_bins[1]["Icosanethiol"].la_over_time
                 ,yerr = data_bins[1]["Icosanethiol"].la_over_time_standard_error
                 ,label = "Icosanethiol"
        )
    axs7.errorbar(data_bins[1]["Tetracosanethiol"].all_replicas[0].frame_over_time/100-2.5
                 ,data_bins[1]["Tetracosanethiol"].la_over_time
                 ,yerr = data_bins[1]["Tetracosanethiol"].la_over_time_standard_error
                 ,label = "Tetracosanethiol"
        )
    
    axs7.set_yticks(np.arange(0, 1.2, step=0.2))
    axs7.tick_params(axis='y', labelsize=15)
    axs7.tick_params(axis='x', labelsize=15)
    axs7.set_ylabel(r'$\langle F_{a} \rangle$',size=15)
    axs7.set_xlabel(r'Time $\mu s$',size=15)
    axs7.legend()
    
    ### Largest Aggregate Over Time Soft Sphere ####
    axs8.errorbar(data_bins[2]["Octanethiol"].all_replicas[0].frame_over_time/100-2.5
                 ,data_bins[2]["Octanethiol"].la_over_time
                 ,yerr = data_bins[2]["Octanethiol"].la_over_time_standard_error
                 ,label = "Octanethiol"
        )
    axs8.errorbar(data_bins[2]["Dodecanthiol"].all_replicas[1].frame_over_time/100-2.5
                 ,data_bins[2]["Dodecanthiol"].la_over_time
                 ,yerr = data_bins[2]["Dodecanthiol"].la_over_time_standard_error
                 ,label = "Dodecanthiol"
        )
    axs8.errorbar(data_bins[2]["Hexadecanethiol"].all_replicas[0].frame_over_time/100-2.5
                 ,data_bins[2]["Hexadecanethiol"].la_over_time
                 ,yerr = data_bins[2]["Hexadecanethiol"].la_over_time_standard_error
                 ,label = "Hexadecanethiol"
        )
    axs8.errorbar(data_bins[2]["Icosanethiol"].all_replicas[0].frame_over_time/100-2.5
                 ,data_bins[2]["Icosanethiol"].la_over_time
                 ,yerr = data_bins[2]["Icosanethiol"].la_over_time_standard_error
                 ,label = "Icosanethiol"
        )
    axs8.errorbar(data_bins[2]["Tetracosanethiol"].all_replicas[0].frame_over_time/100-2.5
                 ,data_bins[2]["Tetracosanethiol"].la_over_time
                 ,yerr = data_bins[2]["Tetracosanethiol"].la_over_time_standard_error
                 ,label = "Tetracosanethiol"
        )
    
    axs8.set_yticks(np.arange(0, 1.2, step=0.2))
    axs8.tick_params(axis='y', labelsize=15)
    axs8.tick_params(axis='x', labelsize=15)
    axs8.set_ylabel(r'$\langle F_{a} \rangle$',size=15)
    axs8.set_xlabel(r'Time $\mu s$',size=15)
    axs8.legend()