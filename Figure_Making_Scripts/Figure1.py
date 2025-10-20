#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 09:34:48 2025

@author: jje63
"""
import sys
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
sys.path.insert(0, "../Analysis/Figure_3_scripts/")
from ClusterPlotter import generalCluster, multiClusterData 

Pagelength = 9
Pagewidth = 6.5

############### Draw Grid ##############

figlength = Pagelength/2
figwidth=Pagewidth
top_bottom_margin=0.125
left_right_margin=0.25
middle_margin=1.375
bumper = 0.40
Annotation = ['a)','b)','c)']

leftside = left_right_margin/figwidth
rightside = 1-(left_right_margin/figwidth)
topside = 1-(top_bottom_margin/figlength)
middle = (top_bottom_margin+middle_margin)/figlength
bottommiddle = middle-bumper
topmiddle = bottommiddle+bumper+.1
bottomside = top_bottom_margin/figlength  

fig = plt.figure(figsize=(figwidth, figlength), tight_layout=True)
gs1 = fig.add_gridspec(nrows=2, ncols=3, figure=fig, wspace=.05)
gs1.update(left=leftside, right=rightside, top=topside, bottom=bottommiddle )
ax1 = fig.add_subplot(gs1[0, 0])
ax2 = fig.add_subplot(gs1[0, 1], sharey=ax1)
ax3 = fig.add_subplot(gs1[0, 2], sharey=ax2)

gs2 = fig.add_gridspec(nrows=1, ncols=2, figure=fig)
gs2.update(left=leftside, right=rightside, top=topmiddle, bottom=bottomside)
ax4 = fig.add_subplot(gs2[0])
ax5 = fig.add_subplot(gs2[1])

fig.text(
   -0.04,
    0.95,
    Annotation[0],
    )

fig.text(
   -0.04,
    0.45,
    Annotation[1],
    )

fig.text(
    0.47,
    0.45,
    Annotation[2],
    )


############# Import Images #############
Figure1 = Path("../Media/Figure1/Polar.png")
Figure2 = Path("../Media/Figure1/Hydrophobic.png")
Figure3 = Path("../Media/Figure1/SoftSphere.png")
Polar10npimage = np.asarray(Image.open(Figure1))
Hydrophobic10npimage = np.asarray(Image.open(Figure2))
SoftSphere10npimage = np.asarray(Image.open(Figure3))

############# Making plottable Cluster Data #############
basepath = Path("../Simulation/Multi_Nanoparticle/10_NP_Systems")
sub_dir_base = ["Hydrophobic","Polar","Soft_Sphere" ]
thiol_name = ["Octanethiol", "Dodecanethiol","Hexadecanethiol","Icosanethiol","Tetracosanethiol"]
file_name = "analysis/ClusterAU10.dat"
#data_bins = {}
data_bins = [{},{},{}]

for i in range(len(sub_dir_base)):
        bins = data_bins[i]
        for j in range(len(thiol_name)):
            paths = basepath.glob(sub_dir_base[i]+"*/"+thiol_name[j]+"/Replica_[1-5]/"+file_name)
            data = multiClusterData(paths)
            bins[thiol_name[j]] = data

############# Plot on Grid #############
my_font = {'family': 'serif',
           'color':  'black',
           'weight': 'normal',
           'size': 10}
LWidth = 1
LStyle = 'solid'
MSize = 5
CSize = 4 
Ligand_Lengths = [8,12,16,20,24]
hydrophobic_color = "#003dfc"
polar_color = "#fc8900"
softsphere_color = "grey"


    ################## Images ####################
ax1.imshow(Polar10npimage)
ax1.set_aspect('auto')
ax1.axis('off')
ax2.imshow(Hydrophobic10npimage)
ax2.set_aspect('auto')
ax2.axis('off')
ax3.imshow(SoftSphere10npimage)
ax3.set_aspect('auto')
ax3.axis('off')

    ################## Largest Aggregate Fraction ####################
ax4.errorbar(Ligand_Lengths,
                 [data_bins[0]["Octanethiol"].all_la_fraction
                 ,data_bins[0]["Dodecanethiol"].all_la_fraction
                 ,data_bins[0]["Hexadecanethiol"].all_la_fraction
                 ,data_bins[0]["Icosanethiol"].all_la_fraction
                 ,data_bins[0]["Tetracosanethiol"].all_la_fraction
                  ],
                 yerr=[data_bins[0]["Octanethiol"].la_standard_error
                      ,data_bins[0]["Dodecanethiol"].la_standard_error
                      ,data_bins[0]["Hexadecanethiol"].la_standard_error
                      ,data_bins[0]["Icosanethiol"].la_standard_error
                      ,data_bins[0]["Tetracosanethiol"].la_standard_error
                     ]
                ,linestyle=LStyle
                ,linewidth=LWidth
                ,marker='o'
                ,alpha=0.5
                ,markersize=MSize
                ,capsize=CSize
                ,color=hydrophobic_color
                ,label="Hydrophobic"
        )

ax4.errorbar(Ligand_Lengths,
                 [data_bins[1]["Octanethiol"].all_la_fraction
                 ,data_bins[1]["Dodecanethiol"].all_la_fraction
                 ,data_bins[1]["Hexadecanethiol"].all_la_fraction
                 ,data_bins[1]["Icosanethiol"].all_la_fraction
                 ,data_bins[1]["Tetracosanethiol"].all_la_fraction
                  ],
                 yerr=[data_bins[1]["Octanethiol"].la_standard_error
                      ,data_bins[1]["Dodecanethiol"].la_standard_error
                      ,data_bins[1]["Hexadecanethiol"].la_standard_error
                      ,data_bins[1]["Icosanethiol"].la_standard_error
                      ,data_bins[1]["Tetracosanethiol"].la_standard_error
                     ]
                ,linestyle=LStyle
                ,linewidth=LWidth
                , marker='^'
                ,markersize=MSize
                ,capsize=CSize
                ,color=polar_color
                ,label="Polar"
        )
    

ax4.errorbar(Ligand_Lengths,
                 [data_bins[2]["Octanethiol"].all_la_fraction
                 ,data_bins[2]["Dodecanethiol"].all_la_fraction
                 ,data_bins[2]["Hexadecanethiol"].all_la_fraction
                 ,data_bins[2]["Icosanethiol"].all_la_fraction
                 ,data_bins[2]["Tetracosanethiol"].all_la_fraction
                  ],
                 yerr=[data_bins[2]["Octanethiol"].la_standard_error
                      ,data_bins[2]["Dodecanethiol"].la_standard_error
                      ,data_bins[2]["Hexadecanethiol"].la_standard_error
                      ,data_bins[2]["Icosanethiol"].la_standard_error
                      ,data_bins[2]["Tetracosanethiol"].la_standard_error
                     ]
                , linestyle=LStyle
                ,linewidth=LWidth
                ,marker='o'
                ,markersize=MSize
                ,capsize=CSize
                ,color=softsphere_color
                ,label="Soft Sphere"
        )

ax4.set_yticks(np.arange(0, 1.2, step=0.2))
ax4.set_xticks(Ligand_Lengths)
ax4.set_yticklabels(["$0.0$","$0.2$","$0.4$","$0.6$","$0.8$","$1.0$"],fontdict=my_font)
ax4.set_xticklabels(Ligand_Lengths,fontdict=my_font)
ax4.set_ylabel(r'$\langle F_{a} \rangle$',fontdict=my_font)
ax4.set_xlabel('Ligand Length',fontdict=my_font)
ax4.legend(loc="upper right",fontsize='x-small')

    ################## Monomer Fraction ##################
    
ax5.errorbar(Ligand_Lengths,
                 [data_bins[0]["Octanethiol"].all_monomer_fraction
                 ,data_bins[0]["Dodecanethiol"].all_monomer_fraction
                 ,data_bins[0]["Hexadecanethiol"].all_monomer_fraction
                 ,data_bins[0]["Icosanethiol"].all_monomer_fraction
                 ,data_bins[0]["Tetracosanethiol"].all_monomer_fraction
                  ],
                 yerr=[data_bins[0]["Octanethiol"].monomer_standard_error
                      ,data_bins[0]["Dodecanethiol"].monomer_standard_error
                      ,data_bins[0]["Hexadecanethiol"].monomer_standard_error
                      ,data_bins[0]["Icosanethiol"].monomer_standard_error
                      ,data_bins[0]["Tetracosanethiol"].monomer_standard_error
                     ]
                ,linestyle=LStyle
                ,linewidth=LWidth
                ,marker='o'
                ,alpha=0.5
                ,markersize=MSize
                ,capsize=8
                ,color=hydrophobic_color
                ,label="Hydrophobic"
        )
    
    
ax5.errorbar(Ligand_Lengths,
                 [data_bins[1]["Octanethiol"].all_monomer_fraction
                 ,data_bins[1]["Dodecanethiol"].all_monomer_fraction
                 ,data_bins[1]["Hexadecanethiol"].all_monomer_fraction
                 ,data_bins[1]["Icosanethiol"].all_monomer_fraction
                 ,data_bins[1]["Tetracosanethiol"].all_monomer_fraction
                  ],
                 yerr=[data_bins[1]["Octanethiol"].monomer_standard_error
                      ,data_bins[1]["Dodecanethiol"].monomer_standard_error
                      ,data_bins[1]["Hexadecanethiol"].monomer_standard_error
                      ,data_bins[1]["Icosanethiol"].monomer_standard_error
                      ,data_bins[1]["Tetracosanethiol"].monomer_standard_error
                     ]
                ,linestyle=LStyle
                ,linewidth=LWidth
                , marker='^'
                ,markersize=MSize
                ,capsize=8
                ,color=polar_color
                ,label="Polar"
        )

ax5.errorbar(Ligand_Lengths,
                 [data_bins[2]["Octanethiol"].all_monomer_fraction
                 ,data_bins[2]["Dodecanethiol"].all_monomer_fraction
                 ,data_bins[2]["Hexadecanethiol"].all_monomer_fraction
                 ,data_bins[2]["Icosanethiol"].all_monomer_fraction
                 ,data_bins[2]["Tetracosanethiol"].all_monomer_fraction
                  ],
                 yerr=[data_bins[2]["Octanethiol"].monomer_standard_error
                      ,data_bins[2]["Dodecanethiol"].monomer_standard_error
                      ,data_bins[2]["Hexadecanethiol"].monomer_standard_error
                      ,data_bins[2]["Icosanethiol"].monomer_standard_error
                      ,data_bins[2]["Tetracosanethiol"].monomer_standard_error
                     ]
                , linestyle=LStyle
                ,linewidth=LWidth
                ,marker='o'
                ,markersize=MSize
                ,capsize=8
                ,color=softsphere_color
                ,label="Soft Sphere"
        )

ax5.set_yticks(np.arange(0, 1.2, step=0.2))
ax5.set_xticks(Ligand_Lengths)
ax5.set_yticklabels(["$0.0$","$0.2$","$0.4$","$0.6$","$0.8$","$1.0$"],fontdict=my_font)
ax5.set_xticklabels(Ligand_Lengths,fontdict=my_font)
ax5.set_ylabel(r'$\langle F_{m} \rangle$',fontdict=my_font)
ax5.set_xlabel('Ligand Length',fontdict=my_font)
ax5.legend(loc="upper right",fontsize='x-small')

fig.savefig(Path("../Graphs/Figure1.pdf"),format='pdf',dpi=500, bbox_inches='tight')
plt.show()