#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 09:34:48 2025

@author: jje63
"""

import numpy as np
import matplotlib.pyplot as plt

Pagelength = 9
Pagewidth = 6.5

figlength = Pagelength/3
figwidth=Pagewidth
top_bottom_margin=0.125
left_right_margin=0.25
middle_margin=1.375
bumper = 0.30

leftside = left_right_margin/figwidth
rightside = 1-(left_right_margin/figwidth)
topside = 1-(top_bottom_margin/figlength)
middle = (top_bottom_margin+middle_margin)/figlength
bottommiddle = middle-bumper
topmiddle = bottommiddle+bumper
bottomside = top_bottom_margin/figlength

print([f"left: {leftside}", f"right: {rightside}"])
print([f"top: {topside}", f"middlebottom: {bottommiddle}"])
print([f"top: {topmiddle}", f"middlebottom: {bottomside}"])       

fig = plt.figure(figsize=(figwidth, figlength), tight_layout=True)
gs1 = fig.add_gridspec(nrows=2, ncols=3, figure=fig)
gs1.update(left=leftside, right=rightside, top=topside, bottom=bottommiddle )
ax1 = fig.add_subplot(gs1[0, 0])
ax2 = fig.add_subplot(gs1[0, 1])
ax3 = fig.add_subplot(gs1[0, 2])

gs2 = fig.add_gridspec(nrows=1, ncols=2, figure=fig)
gs2.update(left=leftside, right=rightside, top=topmiddle, bottom=bottomside)
ax4 = fig.add_subplot(gs2[0])
ax5 = fig.add_subplot(gs2[1])


plt.show()