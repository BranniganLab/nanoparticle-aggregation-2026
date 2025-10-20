#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 11:34:30 2022

@author: jje63
"""
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt
import seaborn as sns
from scipy.stats.kde import gaussian_kde
import scipy.interpolate as interpolate
import math


def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


def AverageSASA(SASAData):
    SASAavg = []
    for item in list(SASAData.values()):
        #print(item[1])
        SASAavg.append(item[1])
        SASAavg2 = np.array(SASAavg[0])
        #print(SASAavg2)
        SASAavg3 = np.average(SASAavg2, axis=0)
    return SASAavg3


def ParseSASAInformation(FolderPath):
    Files = "".join((FolderPath, "/SASA??.dat"))
    Counter = 1
    NPDict = {}
    for name in glob.glob(Files):
        # print(name)
        File1 = open(name, "r")
        Frame = []
        SASA = []
        for line in File1:
            line = line.split()
            Frame.append(float(line[0])/100)
            SASA.append(float(line[1])/10)
        NPDict["".join(("NP", str(Counter)))] = [Frame, SASA]
        Counter += 1
    return NPDict

def ParseDistanceInformation(FilePath):
    File1 = open(FilePath, "r")
    Frame = []
    dist = []
    for line in File1:
        sline = line.split()
        Frame.append(int(sline[0])/100)
        dist.append(float(sline[1]))
    return [Frame,dist]

def ParseFaggInformation(FilePath):
    File1 = open(FilePath, "r")
    Frame = []
    Faggr = []
    for line in File1:
        if line.split()[0] == "Frame":
            Frame.append(int(line.split()[1]))
        elif line.split()[0] == "line11" or line.split()[0] == "line6":
            pass
        else:
            L1 = line.split()
            #print(L1)
            L1 = [int(i) for i in L1]
            Faggr.append(max(L1))
    return [Frame, Faggr]


def ParseClusterInformation(ClusterFilePath):
    LargestAggregateFraction = []
    MonomerFraction = []
    Frame = []
    AllAggregateSizes = []
    Aggregates = []
    ClusterFilePath = open(ClusterFilePath)
    for line in ClusterFilePath:
        sline = line.replace("\n", "").replace(" ", "\n", 1).replace(
            " {{", "\n").replace("}}", "").replace(" {", "\n").replace("}", "")
        sline2 = sline.split()[1]
        if sline2.isnumeric() == True:
            sl = sline.split("\n")
        elif sline2 == "{":
            sline = sline.replace("{", "", 1).replace("}", "", 1)
            sl = sline.split("\n")
        else:
            sline = sline.replace("{", "")
            sl = sline.split("\n")
        Frame.append(int(sl[0]))
        if sl[1] == "":
            MonomerFraction.append(0)
        else:
            NumberList = ConvertStringListToNumList(sl[1])
            Monomers = np.count_nonzero(NumberList)
            MonomerFraction.append(Monomers)

        LargestAggregateFraction.append(max(ConvertAggregateData(sl[2:])))

        if sl[1] != "":
            data = np.concatenate(
                [np.ones(np.count_nonzero(NumberList)), ConvertAggregateData(sl[2:])])
            AllAggregateSizes.append(np.mean(data))
            for num in data:
                Aggregates.append(num)
        else:
            data = ConvertAggregateData(sl[2:])
            AllAggregateSizes.append(np.mean(data))
            for num in data:
                Aggregates.append(num)
    return [Frame, LargestAggregateFraction, MonomerFraction, AllAggregateSizes, Aggregates]


def ConvertStringListToNumList(NumberString):
    StringList = NumberString.split()
    NumList = [eval(i) for i in StringList]
    return NumList


def ConvertAggregateData(NumberString):
    TempList = []
    for string in NumberString:
        NumList = ConvertStringListToNumList(string)
        TempList.append(np.count_nonzero(NumList))
    return TempList

def ParseMonInformation(FilePath):
    File1 = open(FilePath, "r")
    Frame = []
    Mono = []
    Monoful = []
    for line in File1:
        if line.split()[0] == "Frame":
            Frame.append(int(line.split()[1]))
        elif line.split()[0] == "line11":
            pass
        else:
            L1 = line.split()
            for i in L1:
                if int(i) == 1:
                    Mono.append(int(i))
            L2 = sum(Mono)/10
            Monoful.append(L2)
            Mono = []
    return [Frame, Monoful]


def ParseRgyrInformation(FilePath):
    File1 = open(FilePath, "r")
    Rgyr = []
    leng = []
    for line in File1:
        if line.split()[0] == "rgyl":
            pass
        elif line.split()[0] == "leng": 
            leng.append(math.sqrt(float(line.split()[1])))
             
        else:
            Rgyr.append(max([float(x) for x in line.split()]))
    return [Rgyr,leng]


def ParseOrdInformation(FilePath):
    File1 = open(FilePath, "r")
    Order = []
    for line in File1:
        Order.append(float(line.split()[2]))
    return Order


def ParseLCInformation(FilePath):
    File1 = open(FilePath, "r")
    Frame = []
    LC = []
    for line in File1:
        if line.split()[0].startswith("@"):
            pass
        elif line.split()[0].startswith("&"):
            pass
        else:
            Frame.append(int(line.split()[0]))
            LC.append(float(line.split()[1]))
    return [Frame, LC]


def ParseWCInformation(FilePath):
    File1 = open(FilePath, "r")
    Frame = []
    WC = []
    for line in File1:
        if line.split()[0].startswith("@"):
            pass
        elif line.split()[0].startswith("&"):
            pass
        else:
            Frame.append(int(line.split()[0]))
            WC.append(float(line.split()[1]))
    return [Frame, WC]

def ParseWC_LCInformation(FilePath):
    File1 = open(FilePath, "r")
    Frame = []
    WC = []
    LC = []
    for line in File1:
        Frame.append(int(line.split()[0]))
        WC.append(int(line.split()[1]))
        LC.append(int(line.split()[2]))
    return [Frame,WC,LC]

def ParseContactFreqInformation(FilePath):
    File1 = open(FilePath, "r")
    Frame = 0
    ContactArray=[]
    Contactdict={}
    Names = []
    for line in File1:
        sline = line.split()
        if sline[1] not in Contactdict.keys():
            Contactdict[sline[1]]=0
        if int(sline[0]) != Frame:
            if Frame != 0:
                sumarray=sum(ContactArray)
                fractarray=np.array(ContactArray)/sumarray
                for i in range(len(fractarray)):
                    if Contactdict[Names[i]]!=0:
                        Contactdict[Names[i]]=(Contactdict[Names[i]]+fractarray[i])/2
                    else:
                        Contactdict[Names[i]]=fractarray[i]
                Frame = int(sline[0])
                ContactArray=[int(sline[2])]
                Names = [sline[1]]
            elif Frame == 0:
                Frame = int(sline[0])
                ContactArray=[int(sline[2])]
                Names.append(sline[1])
                #print (int(sline[2]))
                #print(Frame,ContactArray,Names)
        else: 
            Frame = int(sline[0])
            ContactArray.append(int(sline[2]))
            Names.append(sline[1])
    return Contactdict

def ParseOrderParamTimeInformation(FolderPath, Multiplier):
    Files = "".join((FolderPath, "/Ord??.dat"))
    Counter = 0
    Time = []
    Ord = []
    for name in glob.glob(Files):
        # print(name)
        File1 = open(name, "r")
        for line in File1:
            line = line.split()
            Time.append(Counter*Multiplier/100)
            Ord.append(float(line[2]))
        Counter += 1
    return [Time,Ord]
            
    
#Hex1 = ParseSASAInformation("/media/jje63/easystore/Coverage/100Dodecanethiol")
#Agg1 = ParseFaggInformation("/media/jje63/easystore/Coverage/100Dodecanethiol/cluster6.dat")
#LC1 = ParseLCInformation("/media/jje63/easystore/Coverage/100Dodecanethiol/LipidcoordinationGNPrid5.agr")
#WC1 = ParseWCInformation("/media/jje63/easystore/Coverage/100Dodecanethiol/WatercoordinationGNPrid5.agr")
#Hexavg = AverageSASA(Hex1)

# print(Hex1)
font = {'family':'serif',
        'weight':'normal',
        'size': 20,
        }
font2 = {'family':'serif',
        'weight':'normal',
        'size': 12,
        }

### Fagg Aggregation Ligand Length ###

"""
Oct = ParseFaggInformation("/media/jje63/easystore1/Octanethiol/cluster11.dat")
Oct1 =ParseFaggInformation("/media/jje63/easystore1/Octanethiol_1/cluster11.dat")
Oct2 =ParseFaggInformation("/media/jje63/easystore1/Octanethiol_2/cluster11.dat")
Dod =ParseFaggInformation("/media/jje63/easystore1/NP_Concentration/10np_membrane_3/cluster11.dat")
Dod1 =ParseFaggInformation("/media/jje63/easystore1/NP_Concentration/10np_membrane_4/cluster11.dat")
Dod2 =ParseFaggInformation("/media/jje63/easystore1/NP_Concentration/10np_membrane_5/cluster11.dat")
#Dodx =ParseFaggInformation("/media/jje63/easystore/NP_Concentration/10np_membrane_4/cluster11.dat")
Hex =ParseFaggInformation("/media/jje63/easystore1/Hexadecanethiol/cluster11.dat")
Hex1 =ParseFaggInformation("/media/jje63/easystore1/Hexadecanethiol_1/cluster11.dat")
Hex2 =ParseFaggInformation("/media/jje63/easystore1/Hexadecanethiol_2/cluster11.dat")
Ico =ParseFaggInformation("/media/jje63/easystore1/Icosanethiol/cluster11.dat")
Ico1 =ParseFaggInformation("/media/jje63/easystore1/Icosanethiol_1/cluster11.dat")
Ico2 =ParseFaggInformation("/media/jje63/easystore1/Icosanethiol_2/cluster11.dat")
Tetco =ParseFaggInformation("/media/jje63/easystore1/Bridges2/jennis/Tetracosanethiol/tetracosanethiol_1/cluster11.dat")
Tetco1 =ParseFaggInformation("/media/jje63/easystore1/Bridges2/jennis/Tetracosanethiol/tetracosanethiol_2/cluster11.dat")
Tetco2 =ParseFaggInformation("/media/jje63/easystore1/Bridges2/jennis/Tetracosanethiol/tetracosanethiol_3/cluster11.dat")


xvalsOct = np.array([max(Oct[1][20:])/10,max(Oct1[1][20:])/10,max(Oct2[1][20:])/10])
xvalsDod = np.array([max(Dod[1][20:])/10,max(Dod1[1][20:])/10,max(Dod2[1][20:])/10])
#xvalsDod = np.array([max(Dodx[1][20:])/10])
xvalsHex = np.array([max(Hex[1][20:])/10,max(Hex1[1][20:])/10,max(Hex2[1][20:])/10])
xvalsIco = np.array([max(Ico[1][20:])/10,max(Ico1[1][20:])/10,max(Ico2[1][20:])/10])
xvalsTetco = np.array([max(Tetco[1][20:])/10+.126,max(Tetco1[1][20:])/10+.126,max(Tetco2[1][20:])/10+.126])

AvgOct = np.mean(xvalsOct)
AvgDod = np.mean(xvalsDod)
AvgHex = np.mean(xvalsHex)
AvgIco = np.mean(xvalsIco)
AvgTetco = np.mean(xvalsTetco)
AllAvg = [AvgOct,AvgDod,AvgHex,AvgIco,AvgTetco]

StdOct = np.std(xvalsOct)/math.sqrt(3)
StdDod = np.std(xvalsDod)/math.sqrt(3)
StdHex = np.std(xvalsHex)/math.sqrt(3)
StdIco = np.std(xvalsIco)/math.sqrt(3)
StdTetco = np.std(xvalsTetco)/math.sqrt(3)
AllStd = [StdOct,StdDod,StdHex,StdIco,StdTetco]

Cbare = ParseClusterInformation("/media/jje63/My Passport/bareMulti/ClusterAU35.dat")
COct = ParseFaggInformation("/media/jje63/easystore1/Multinano_C1_2/Octanethiol_C1/cluster11.dat")
COct1 =ParseFaggInformation("/media/jje63/easystore1/Bridges2/jennis/C1_Nano/Octanethiol_P1/cluster11.dat")
COct2 =ParseFaggInformation("/media/jje63/easystore1/Bridges2/jennis/C1_Nano_2/Octanethiol_P1/cluster11.dat")
CDod =ParseFaggInformation("/media/jje63/easystore1/Multinano_C1_2/Dodecanethiol_C1/cluster11.dat")
CDod1 =ParseFaggInformation("/media/jje63/easystore1/Bridges2/jennis/C1_Nano/Dodecanethiol_C1/cluster11.dat")
CDod2 =ParseFaggInformation("/media/jje63/easystore1/Bridges2/jennis/C1_Nano_2/Dodecanethiol_C1/cluster11.dat")
CHex =ParseFaggInformation("/media/jje63/easystore1/Multinano_C1_2/Hexadecanethiol_C1/cluster11.dat")
CHex1 =ParseFaggInformation("/media/jje63/easystore1/Bridges2/jennis/C1_Nano/Hexadecanethiol_C1/cluster11.dat")
CHex2 =ParseFaggInformation("/media/jje63/easystore1/Bridges2/jennis/C1_Nano_2/Hexadecanethiol_C1/cluster11.dat")
CIco =ParseFaggInformation("/media/jje63/easystore1/Multinano_C1_2/Icotest/cluster11.dat")
CIco1 =ParseFaggInformation("/media/jje63/easystore1/Bridges2/jennis/C1_Nano/Icosanethiol_C1/cluster11.dat")
CIco2 =ParseFaggInformation("/media/jje63/easystore1/Bridges2/jennis/C1_Nano_2/Icosanethiol_C1/cluster11.dat")
CTetco =ParseFaggInformation("/media/jje63/easystore1/Bridges2/jennis/Tetracosanethiol/tetracosanethiol_1C/cluster11.dat")
CTetco1 =ParseFaggInformation("/media/jje63/easystore1/Bridges2/jennis/Tetracosanethiol/tetracosanethiol_2C/cluster11.dat")
CTetco2 =ParseFaggInformation("/media/jje63/easystore1/Bridges2/jennis/Tetracosanethiol/tetracosanethiol_3C/cluster11.dat")

CxvalsBare = np.array([max(Cbare[1][20:])/10])
CxvalsOct = np.array([max(COct[1][20:])/10,max(COct1[1][20:])/10,max(COct2[1][20:])/10])
CxvalsDod = np.array([max(CDod[1][20:])/10,max(CDod1[1][20:])/10,max(CDod2[1][20:])/10])
CxvalsHex = np.array([max(CHex[1][20:])/10,max(CHex1[1][20:])/10,max(CHex2[1][20:])/10])
CxvalsIco = np.array([max(CIco[1][20:])/10,max(CIco1[1][20:])/10,max(CIco2[1][20:])/10])
CxvalsTetco = np.array([max(CTetco[1][20:])/10+.126,max(CTetco1[1][20:])/10+.126,max(CTetco2[1][20:])/10+.126])


CAvgBare = np.mean(CxvalsBare)
CAvgOct = np.mean(CxvalsOct)
CAvgDod = np.mean(CxvalsDod)
CAvgHex = np.mean(CxvalsHex)
CAvgIco = np.mean(CxvalsIco)
CAvgTetco = np.mean(CxvalsTetco)
CAllAvg = [CAvgOct,CAvgDod,CAvgHex,CAvgIco,CAvgTetco]
#CAllAvg = [CAvgOct,CAvgDod,CAvgHex,CAvgIco,CAvgTetco]

CStdBare = np.std(CxvalsBare)/math.sqrt(1)
CStdOct = np.std(CxvalsOct)/math.sqrt(3)
CStdDod = np.std(CxvalsDod)/math.sqrt(3)
CStdHex = np.std(CxvalsHex)/math.sqrt(3)
CStdIco = np.std(CxvalsIco)/math.sqrt(3)
CStdTetco = np.std(CxvalsTetco)/math.sqrt(3)
CAllStd = [CStdOct,CStdDod,CStdHex,CStdIco,CStdTetco]

TOct = ParseClusterInformation("/media/jje63/easystore/MultinanoTest/Octanethiol/ClusterAU15.dat")
TDod = ParseClusterInformation("/media/jje63/easystore/MultinanoTest/Dodecanethiol/ClusterAU15.dat")
THex = ParseClusterInformation("/media/jje63/easystore/MultinanoTest/Hexadecanethiol/ClusterAU15.dat")
TIco = ParseClusterInformation("/media/jje63/easystore/MultinanoTest/Icosanethiol/ClusterAU15.dat")
TTet = ParseClusterInformation("/media/jje63/easystore/MultinanoTest/Tetracosanethiol/ClusterAU15.dat")

#print(TTet)

TxvalsOct = np.array([max(TOct[1][20:])/10])
TxvalsDod = np.array([max(TDod[1][20:])/10])
TxvalsHex = np.array([max(THex[1][20:])/10])
TxvalsIco = np.array([max(TIco[1][20:])/10])
TxvalsTetco = np.array([max(TTet[1][20:])/10])

TAvgOct = np.mean(TxvalsOct)
TAvgDod = np.mean(TxvalsDod)
TAvgHex = np.mean(TxvalsHex)
TAvgIco = np.mean(TxvalsIco)
TAvgTetco = np.mean(TxvalsTetco)

TAllAvg = [TAvgOct,TAvgDod,TAvgHex,TAvgIco,TAvgTetco]

TStdOct = np.std(TxvalsOct)/math.sqrt(1)
TStdDod = np.std(TxvalsDod)/math.sqrt(1)
TStdHex = np.std(TxvalsHex)/math.sqrt(1)
TStdIco = np.std(TxvalsIco)/math.sqrt(1)
TStdTetco = np.std(TxvalsTetco)/math.sqrt(1)
TAllStd = [TStdOct,TStdDod,TStdHex,TStdIco,TStdTetco]

figure , axs = plt.subplots(2,1, figsize=(8,6), sharex=True)
figure.tight_layout(pad=2)
axs[0].errorbar([8,12,16,20,24], TAllAvg, yerr= TAllStd,linestyle='solid',linewidth=3, marker='X',markersize = 16,capsize=8,color="black",label="Neutral")
axs[0].errorbar([8,12,16,20,24], AllAvg, yerr= AllStd,linestyle='solid',linewidth=3, marker='^',markersize = 13,capsize=8,color="#BA6E6E",label="Charged")
axs[0].errorbar([8,12,16,20,24], CAllAvg, yerr= CAllStd,linestyle='solid',linewidth=3,marker='o',markersize = 13,capsize=8,color="#439FEF",label="Hydrophobic")
axs[0].set_yticks(np.arange(0, 1.2, step=0.2))
axs[0].set_yticklabels(["$0.0$","$0.2$","$0.4$","$0.6$","$0.8$","$1.0$"],fontdict=font2)
axs[0].set_ylabel(r'$\langle F_{a} \rangle$',fontdict=font)
axs[0].set_xlabel('$L_{l}$',fontdict=font)
#axs.legend(loc="upper right",bbox_to_anchor=(1.0, 1.0))
#plt.errorbar([8,12,16,20,24], AllAvg, yerr= AllStd,linestyle='none', marker='^',markersize = 10,color="#BA6E6E",label="Charged Gold Core")
#plt.errorbar([8,12,16,20,24], CAllAvg, yerr= CAllStd,linestyle='none', marker='o',markersize = 8,color="#439FEF",label="Hydrophobic Gold Core")
#plt.yticks(np.arange(0, 1.2, step=0.2))
#plt.legend(loc="upper right",bbox_to_anchor=(1.35, 1.20))
#plt.savefig("/media/jje63/easystore/Graphs/Fagg_LigandLengthall2.pdf",format='pdf',dpi=500, bbox_inches='tight')
"""


### Fagg Aggregation Nanoparticle Size ###

"""
t2nm = ParseFaggInformation("/media/jje63/easystore/NP_Concentration/10np_membrane_3/cluster11.dat")
t2nm1 =ParseFaggInformation("/media/jje63/easystore/NP_Concentration/10np_membrane_4/cluster11.dat")
t2nm2 =ParseFaggInformation("/media/jje63/easystore/NP_Concentration/10np_membrane_5/cluster11.dat")
t3nm =ParseFaggInformation("/media/jje63/My Passport/3nmGNP/cluster11.dat")
t3nm1 =ParseFaggInformation("/media/jje63/easystore/3nmGNP/cluster11.dat")
t3nm2 =ParseFaggInformation("/media/jje63/easystore/3nmGNP_2/cluster11.dat")
t4nm =ParseFaggInformation("/media/jje63/My Passport/4nmGNP/cluster11.dat")
t4nm1 =ParseFaggInformation("/media/jje63/easystore/4nmGNP/cluster11.dat")
t4nm2 =ParseFaggInformation("/media/jje63/easystore/4nmGNP_2/cluster11.dat")
t5nm =ParseFaggInformation("/media/jje63/My Passport/5nmGNP/cluster11.dat")
t5nm1 =ParseFaggInformation("/media/jje63/easystore/5nmGNP/cluster11.dat")
t5nm2 =ParseFaggInformation("/media/jje63/easystore/5nmGNP_2/cluster11.dat")


xvals2nm = np.array([max(t2nm[1][20:])/10,max(t2nm1[1][20:])/10,max(t2nm2[1][20:])/10])
xvals3nm = np.array([max(t3nm[1][20:])/10,max(t3nm1[1][20:])/10,max(t3nm2[1][20:])/10])
xvals4nm = np.array([max(t4nm[1][20:])/10,max(t4nm1[1][20:])/10,max(t4nm2[1][20:])/10])
xvals5nm = np.array([max(t5nm[1][20:])/10,max(t5nm1[1][20:])/10,max(t5nm2[1][20:])/10])


Avg2nm = np.mean(xvals2nm)
Avg3nm = np.mean(xvals3nm)
Avg4nm = np.mean(xvals4nm)
Avg5nm = np.mean(xvals5nm)
AllAvg = [Avg2nm,Avg3nm,Avg4nm,Avg5nm]

Std2nm = np.std(xvals2nm)/math.sqrt(3)
Std3nm = np.std(xvals3nm)/math.sqrt(3)
Std4nm = np.std(xvals4nm)/math.sqrt(3)
Std5nm = np.std(xvals5nm)/math.sqrt(3)
AllStd = [Std2nm,Std3nm,Std4nm,Std5nm]

C2nm = ParseFaggInformation("/media/jje63/easystore/Multinano_C1_2/Dodecanethiol_C1/cluster11.dat")
C2nm1 =ParseFaggInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano/Dodecanethiol_C1/cluster11.dat")
C2nm2 =ParseFaggInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano_2/Dodecanethiol_C1/cluster11.dat")
C3nm =ParseFaggInformation("/media/jje63/easystore/Bridges2/jennis/Bending_Carb/3nm_C1/cluster11.dat")
C3nm1 =ParseFaggInformation("/media/jje63/easystore/Bridges2/jennis/Bending_Carb/3nm_C2/cluster11.dat")
C3nm2 =ParseFaggInformation("/media/jje63/easystore/Bridges2/jennis/Bending_Carb/3nm_C3/cluster11.dat")
C4nm =ParseFaggInformation("/media/jje63/easystore/Bridges2/jennis/Bending_Carb/4nm_C1/cluster11.dat")
C4nm1 =ParseFaggInformation("/media/jje63/easystore/Bridges2/jennis/Bending_Carb/4nm_C2/cluster11.dat")
C4nm2 =ParseFaggInformation("/media/jje63/easystore/Bridges2/jennis/Bending_Carb/4nm_C3/cluster11.dat")
C5nm =ParseFaggInformation("/media/jje63/easystore/Bridges2/jennis/Bending_Carb/5nm_C1/cluster11.dat")
C5nm1 =ParseFaggInformation("/media/jje63/easystore/Bridges2/jennis/Bending_Carb/5nm_C2/cluster11.dat")
C5nm2 =ParseFaggInformation("/media/jje63/easystore/Bridges2/jennis/Bending_Carb/5nm_C3/cluster11.dat")


Cxvals2nm = np.array([max(C2nm[1][20:])/10,max(C2nm1[1][20:])/10,max(C2nm2[1][20:])/10])
Cxvals3nm = np.array([max(C3nm[1][20:])/10,max(C3nm1[1][20:])/10,max(C3nm2[1][20:])/10])
Cxvals4nm = np.array([max(C4nm[1][20:])/10,max(C4nm1[1][20:])/10,max(C4nm2[1][20:])/10])
Cxvals5nm = np.array([max(C5nm[1][20:])/10,max(C5nm1[1][20:])/10,max(C5nm2[1][20:])/10])


CAvg2nm = np.mean(Cxvals2nm)
CAvg3nm = np.mean(Cxvals3nm)
CAvg4nm = np.mean(Cxvals4nm)
CAvg5nm = np.mean(Cxvals5nm)
CAllAvg = [CAvg2nm,CAvg3nm,CAvg4nm,CAvg5nm]


CStd2nm = np.std(Cxvals2nm)/math.sqrt(3)
CStd3nm = np.std(Cxvals3nm)/math.sqrt(3)
CStd4nm = np.std(Cxvals4nm)/math.sqrt(3)
CStd5nm = np.std(Cxvals5nm)/math.sqrt(3)
CAllStd = [CStd2nm,CStd3nm,CStd4nm,CStd5nm]

All = [Avg2nm,Avg3nm,Avg4nm,Avg5nm,CStd2nm,CStd3nm,CStd4nm,CStd5nm]

figure , axs = plt.subplots(1, figsize=(8,6), sharex=True)
figure.tight_layout(pad=2)
#axs.errorbar([2,3,4,5], AllAvg, yerr= AllStd,linestyle='dotted',linewidth=3, marker='^',markersize = 13,capsize=8,color="#BA6E6E",label="Charged Core")
axs.errorbar([2,3,4,5], CAllAvg, yerr= CAllStd,linestyle='dotted',linewidth=3, marker='o',markersize = 13,capsize=8,color="#439FEF",label="Hydrophobic Core")
axs.set_yticks(np.arange(0, 1.2, step=0.2))
axs.set_yticklabels(["$0.0$","$0.2$","$0.4$","$0.6$","$0.8$","$1.0$"],fontdict=font2)
axs.set_ylabel('$<F_{a}>$',fontdict=font)
axs.set_xlabel('$N_{s}$ ($nm$)')
#axs.legend(loc="upper right",bbox_to_anchor=(1.0, 1.0))
plt.savefig("/media/jje63/easystore/Graphs/Fagg_NPsizehydrophobic.pdf",format='pdf',dpi=500, bbox_inches='tight')
"""

### Fagg Coverage ###

"""
Dod100 = ParseFaggInformation("/media/jje63/easystore/Coverage/100Dodecanethiol/cluster6.dat")
Dod80 = ParseFaggInformation("/media/jje63/easystore/Coverage/80Dodecanethiol/cluster6.dat")
Dod70 = ParseFaggInformation("/media/jje63/easystore/Coverage/70Dodecanethiol/cluster6.dat")
Dod60 = ParseFaggInformation("/media/jje63/easystore/Coverage/60Dodecanethiol/cluster6.dat")
Dod40 = ParseFaggInformation("/media/jje63/easystore/Coverage/40Dodecanethiol/cluster6.dat")
#Dod20 = ParseFaggInformation("/media/jje63/easystore/Coverage/20Dodecanethiol/cluster6.dat")

xvals100 = np.mean(Dod100[1][200:])/5
xvals80 = np.mean(Dod80[1][200:])/5
xvals70 = np.mean(Dod70[1][200:])/5
xvals60 = np.mean(Dod60[1][200:])/5
xvals40 = np.mean(Dod40[1][200:])/5
#xvals20 = max(Dod20[1][20:])/5
print(Dod60[1])

All = [xvals40,xvals60,xvals70,xvals80,xvals100]

plt.plot([40,60,70,80,100],All,linestyle='None',marker='^',markersize = 10,color="orange",label="Charged Gold Core")

plt.savefig("/media/jje63/easystore/Graphs/Fagg_Coverage.pdf",format='pdf',dpi=500, bbox_inches='tight')
"""

### Rgyr Coverage ###

"""
Dod100 = ParseRgyrInformation("/media/jje63/easystore/Coverage/100Dodecanethiol/radiusofgyrationcluster.dat")
Dod80 = ParseRgyrInformation("/media/jje63/easystore/Coverage/80Dodecanethiol/radiusofgyrationcluster.dat")
Dod70 = ParseRgyrInformation("/media/jje63/easystore/Coverage/70Dodecanethiol/radiusofgyrationcluster.dat")
Dod60 = ParseRgyrInformation("/media/jje63/easystore/Coverage/60Dodecanethiol/radiusofgyrationcluster.dat")
Dod40 = ParseRgyrInformation("/media/jje63/easystore/Coverage/40Dodecanethiol/radiusofgyrationcluster.dat")
#Dod20 = ParseRgyrInformation("/media/jje63/easystore/Coverage/20Dodecanethiol/radiusofgyrationcluster.dat")

xvals100 = np.mean(np.array(Dod100[0])/np.array(Dod100[1]))
xvals80 = np.mean(np.array(Dod80)[0]/np.array(Dod80)[1])
xvals70 = np.mean(np.array(Dod70)[0]/np.array(Dod70)[1])
xvals60 = np.mean(np.array(Dod60)[0]/np.array(Dod60)[1])
xvals40 = np.mean(np.array(Dod40)[0]/np.array(Dod40)[1])
#xvals20 = np.mean(np.array(Dod20))/math.sqrt(5)

Oct = ParseRgyrInformation("/media/jje63/easystore/Octanethiol/radiusofgyrationcluster.dat")
Oct1 =ParseRgyrInformation("/media/jje63/easystore/Octanethiol_1/radiusofgyrationcluster.dat")
Oct2 =ParseRgyrInformation("/media/jje63/easystore/Octanethiol_2/radiusofgyrationcluster.dat")
xvalsOct = np.mean(np.array([np.mean(np.array(Oct[0])/np.array(Oct[1])),np.mean(np.array(Oct1[0])/np.array(Oct1[1])),np.mean(np.array(Oct2[0])/np.array(Oct2[1]))]))

All = [xvals40,xvals60,xvalsOct,xvals70,xvals80,xvals100]

plt.plot([40,60,65,70,80,100],All,linestyle='None',marker='^',markersize = 10,color="red",label="Charged Gold Core")
"""

### Monomer Fraction Ligand Length ###

"""
Oct = ParseMonInformation("/media/jje63/easystore1/Octanethiol/cluster11.dat")
Oct1 =ParseMonInformation("/media/jje63/easystore1/Octanethiol_1/cluster11.dat")
Oct2 =ParseMonInformation("/media/jje63/easystore1/Octanethiol_2/cluster11.dat")
Dod =ParseMonInformation("/media/jje63/easystore1/NP_Concentration/10np_membrane_3/cluster11.dat")
Dod1 =ParseMonInformation("/media/jje63/easystore1/NP_Concentration/10np_membrane_4/cluster11.dat")
Dod2 =ParseMonInformation("/media/jje63/easystore1/NP_Concentration/10np_membrane_5/cluster11.dat")
#Dodx =ParseMonInformation("/media/jje63/easystore/NP_Concentration/10np_membrane_4/cluster11.dat")
Hex =ParseMonInformation("/media/jje63/easystore1/Hexadecanethiol/cluster11.dat")
Hex1 =ParseMonInformation("/media/jje63/easystore1/Hexadecanethiol_1/cluster11.dat")
Hex2 =ParseMonInformation("/media/jje63/easystore1/Hexadecanethiol_2/cluster11.dat")
Ico =ParseMonInformation("/media/jje63/easystore1/Icosanethiol/cluster11.dat")
Ico1 =ParseMonInformation("/media/jje63/easystore1/Icosanethiol_1/cluster11.dat")
Ico2 =ParseMonInformation("/media/jje63/easystore1/Icosanethiol_2/cluster11.dat")
Tetco =ParseMonInformation("/media/jje63/easystore1/Bridges2/jennis/Tetracosanethiol/tetracosanethiol_1/cluster11.dat")
Tetco1 =ParseMonInformation("/media/jje63/easystore1/Bridges2/jennis/Tetracosanethiol/tetracosanethiol_2/cluster11.dat")
Tetco2 =ParseMonInformation("/media/jje63/easystore1/Bridges2/jennis/Tetracosanethiol/tetracosanethiol_3/cluster11.dat")

xvalsOct=np.array([np.mean(np.array(Oct[1][200:])),np.mean(np.array(Oct1[1][200:])),np.mean(np.array(Oct2[1][200:]))])
xvalsDod=np.array([np.mean(np.array(Dod[1][200:])),np.mean(np.array(Dod1[1][200:])),np.mean(np.array(Dod2[1][200:]))])
#xvalsDod=np.array([np.mean(np.array(Dodx[1][50:]))])
xvalsHex=np.array([np.mean(np.array(Hex[1][200:])),np.mean(np.array(Hex1[1][200:])),np.mean(np.array(Hex2[1][200:]))])
xvalsIco=np.array([np.mean(np.array(Ico[1][200:])),np.mean(np.array(Ico1[1][200:])),np.mean(np.array(Ico2[1][200:]))])
xvalsTetco=np.array([np.mean(np.array(Tetco[1][200:])),np.mean(np.array(Tetco1[1][200:])),np.mean(np.array(Tetco2[1][200:]))])

AvgOct = np.mean(xvalsOct)
AvgDod = np.mean(xvalsDod)
AvgHex = np.mean(xvalsHex)
AvgIco = np.mean(xvalsIco)
AvgTetco = np.mean(xvalsTetco)
AllAvg = [AvgOct,AvgDod,AvgHex,AvgIco,AvgTetco]

StdOct = np.std(xvalsOct)/math.sqrt(3)
StdDod = np.std(xvalsDod)/math.sqrt(3)
StdHex = np.std(xvalsHex)/math.sqrt(3)
StdIco = np.std(xvalsIco)/math.sqrt(3)
StdTetco = np.std(xvalsTetco)/math.sqrt(3)
AllStd = [StdOct,StdDod,StdHex,StdIco,StdTetco]

COct = ParseMonInformation("/media/jje63/easystore1/Multinano_C1_2/Octanethiol_C1/cluster11.dat")
COct1 =ParseMonInformation("/media/jje63/easystore1/Bridges2/jennis/C1_Nano/Octanethiol_P1/cluster11.dat")
COct2 =ParseMonInformation("/media/jje63/easystore1/Bridges2/jennis/C1_Nano_2/Octanethiol_P1/cluster11.dat")
CDod =ParseMonInformation("/media/jje63/easystore1/Multinano_C1_2/Dodecanethiol_C1/cluster11.dat")
CDod1 =ParseMonInformation("/media/jje63/easystore1/Bridges2/jennis/C1_Nano/Dodecanethiol_C1/cluster11.dat")
CDod2 =ParseMonInformation("/media/jje63/easystore1/Bridges2/jennis/C1_Nano_2/Dodecanethiol_C1/cluster11.dat")
CHex =ParseMonInformation("/media/jje63/easystore1/Multinano_C1_2/Hexadecanethiol_C1/cluster11.dat")
CHex1 =ParseMonInformation("/media/jje63/easystore1/Bridges2/jennis/C1_Nano/Hexadecanethiol_C1/cluster11.dat")
CHex2 =ParseMonInformation("/media/jje63/easystore1/Bridges2/jennis/C1_Nano_2/Hexadecanethiol_C1/cluster11.dat")
CIco =ParseMonInformation("/media/jje63/easystore1/Multinano_C1_2/Icotest/cluster11.dat")
CIco1 =ParseMonInformation("/media/jje63/easystore1/Bridges2/jennis/C1_Nano/Icosanethiol_C1/cluster11.dat")
CIco2 =ParseMonInformation("/media/jje63/easystore1/Bridges2/jennis/C1_Nano_2/Icosanethiol_C1/cluster11.dat")
CTetco =ParseMonInformation("/media/jje63/easystore1/Bridges2/jennis/Tetracosanethiol/tetracosanethiol_1C/cluster11.dat")
CTetco1 =ParseMonInformation("/media/jje63/easystore1/Bridges2/jennis/Tetracosanethiol/tetracosanethiol_2C/cluster11.dat")
CTetco2 =ParseMonInformation("/media/jje63/easystore1/Bridges2/jennis/Tetracosanethiol/tetracosanethiol_3C/cluster11.dat")

CxvalsOct=np.array([np.mean(np.array(COct[1][200:])),np.mean(np.array(COct1[1][200:])),np.mean(np.array(COct2[1][200:]))])
CxvalsDod=np.array([np.mean(np.array(CDod[1][200:])),np.mean(np.array(CDod1[1][200:])),np.mean(np.array(CDod2[1][200:]))])
CxvalsHex=np.array([np.mean(np.array(CHex[1][200:])),np.mean(np.array(CHex1[1][200:])),np.mean(np.array(CHex2[1][200:]))])
CxvalsIco=np.array([np.mean(np.array(CIco[1][200:])),np.mean(np.array(CIco1[1][200:])),np.mean(np.array(CIco2[1][200:]))])
CxvalsTetco=np.array([np.mean(np.array(CTetco[1][200:])-.126),np.mean(np.array(CTetco1[1][200:])-.126),np.mean(np.array(CTetco2[1][200:])-.126)])

CAvgOct = np.mean(CxvalsOct)
CAvgDod = np.mean(CxvalsDod)
CAvgHex = np.mean(CxvalsHex)
CAvgIco = np.mean(CxvalsIco)
CAvgTetco = np.mean(CxvalsTetco)
CAllAvg = [CAvgOct,CAvgDod,CAvgHex,CAvgIco,CAvgTetco]

CStdOct = np.std(CxvalsOct)/math.sqrt(3)
CStdDod = np.std(CxvalsDod)/math.sqrt(3)
CStdHex = np.std(CxvalsHex)/math.sqrt(3)
CStdIco = np.std(CxvalsIco)/math.sqrt(3)
CStdTetco = np.std(CxvalsTetco)/math.sqrt(3)
CAllStd = [CStdOct,CStdDod,CStdHex,CStdIco,CStdTetco]

TOct = ParseClusterInformation("/media/jje63/easystore/MultinanoTest/Octanethiol/ClusterAU25.dat")
TDod = ParseClusterInformation("/media/jje63/easystore/MultinanoTest/Dodecanethiol/ClusterAU25.dat")
THex = ParseClusterInformation("/media/jje63/easystore/MultinanoTest/Hexadecanethiol/ClusterAU25.dat")
TIco = ParseClusterInformation("/media/jje63/easystore/MultinanoTest/Icosanethiol/ClusterAU25.dat")
TTet = ParseClusterInformation("/media/jje63/easystore/MultinanoTest/Tetracosanethiol/ClusterAU25.dat")

#print(THex[2])
TxvalsOct = np.array([np.mean(np.array(TOct[2][200:])/10)])
TxvalsDod = np.array([np.mean(np.array(TDod[2][200:])/10)])
TxvalsHex = np.array([np.mean(np.array(THex[2][200:])/10)])
TxvalsIco = np.array([np.mean(np.array(TIco[2][200:])/10)])
TxvalsTetco = np.array([np.mean(np.array(TTet[2][200:])/10)])


TAvgOct = np.mean(TxvalsOct)
TAvgDod = np.mean(TxvalsDod)
TAvgHex = np.mean(TxvalsHex)
TAvgIco = np.mean(TxvalsIco)
TAvgTetco = np.mean(TxvalsTetco)

TAllAvg = [TAvgOct,TAvgDod,TAvgHex,TAvgIco,TAvgTetco]

TStdOct = np.std(TxvalsOct)/math.sqrt(1)
TStdDod = np.std(TxvalsDod)/math.sqrt(1)
TStdHex = np.std(TxvalsHex)/math.sqrt(1)
TStdIco = np.std(TxvalsIco)/math.sqrt(1)
TStdTetco = np.std(TxvalsTetco)/math.sqrt(1)
TAllStd = [TStdOct,TStdDod,TStdHex,TStdIco,TStdTetco]


#figure , axs = plt.subplots(1, figsize=(8,6), sharex=True)
#figure.tight_layout(pad=2)
axs[1].errorbar([8,12,16,20,24], TAllAvg, yerr= TAllStd,linestyle='solid',linewidth=3, marker='X',markersize = 16,capsize=8,color="black",label="Neutral Core")
axs[1].errorbar([8,12,16,20,24], AllAvg, yerr= AllStd,linestyle='solid',linewidth=3, marker='^',markersize = 13,capsize=8,color="#BA6E6E",label="Polar Core")
axs[1].errorbar([8,12,16,20,24], CAllAvg, yerr= CAllStd,linestyle='solid',linewidth=3, marker='o',markersize = 13,capsize=8,color="#439FEF",label="Hydrophobic Core")
axs[1].set_ylabel('<$M_{f}$>',fontdict=font)
axs[1].set_xlabel('$L_{l}$',fontdict=font)
plt.yticks(np.arange(0, 1.2, step=0.2))
#plt.errorbar([8,12,16,20,24], AllAvg, yerr= AllStd,linestyle='none', marker='^',markersize = 10,color="#BA6E6E",label="Charged Core")
#plt.errorbar([8,12,16,20,24], CAllAvg, yerr= CAllStd,linestyle='none', marker='o',markersize = 8,alpha=.5,color="#439FEF",label="Hydrophobic Core")
#plt.yticks(np.arange(0, 1.2, step=0.2))
#plt.savefig("/media/jje63/easystore/Graphs/MonomerFractionLigandLengthhydrophobic.pdf",format='pdf',dpi=500, bbox_inches='tight')
"""

### Monomer Fraction Nanoparticle Size ###

"""
t2nm = ParseMonInformation("/media/jje63/easystore/NP_Concentration/10np_membrane_3/cluster11.dat")
t2nm1 =ParseMonInformation("/media/jje63/easystore/NP_Concentration/10np_membrane_4/cluster11.dat")
t2nm2 =ParseMonInformation("/media/jje63/easystore/NP_Concentration/10np_membrane_5/cluster11.dat")
t3nm =ParseMonInformation("/media/jje63/My Passport/3nmGNP/cluster11.dat")
t3nm1 =ParseMonInformation("/media/jje63/easystore/3nmGNP/cluster11.dat")
t3nm2 =ParseMonInformation("/media/jje63/easystore/3nmGNP_2/cluster11.dat")
t4nm =ParseMonInformation("/media/jje63/My Passport/4nmGNP/cluster11.dat")
t4nm1 =ParseMonInformation("/media/jje63/easystore/4nmGNP/cluster11.dat")
t4nm2 =ParseMonInformation("/media/jje63/easystore/4nmGNP_2/cluster11.dat")
t5nm =ParseMonInformation("/media/jje63/My Passport/5nmGNP/cluster11.dat")
t5nm1 =ParseMonInformation("/media/jje63/easystore/5nmGNP/cluster11.dat")
t5nm2 =ParseMonInformation("/media/jje63/easystore/5nmGNP_2/cluster11.dat")


xvals2nm = np.array([np.mean(np.array(t2nm[1][50:])),np.mean(np.array(t2nm1[1][50:])),np.mean(np.array(t2nm2[1][50:]))])
xvals3nm = np.array([np.mean(np.array(t3nm[1][20:])),np.mean(np.array(t3nm1[1][20:])),np.mean(np.array(t3nm2[1][20:]))])
xvals4nm = np.array([np.mean(np.array(t4nm[1][20:])),np.mean(np.array(t4nm1[1][20:])),np.mean(np.array(t4nm2[1][20:]))])
xvals5nm = np.array([np.mean(np.array(t5nm[1][20:])),np.mean(np.array(t5nm1[1][20:])),np.mean(np.array(t5nm2[1][20:]))])


Avg2nm = np.mean(xvals2nm)
Avg3nm = np.mean(xvals3nm)
Avg4nm = np.mean(xvals4nm)
Avg5nm = np.mean(xvals5nm)
AllAvg = [Avg2nm,Avg3nm,Avg4nm,Avg5nm]

Std2nm = np.std(xvals2nm)/math.sqrt(3)
Std3nm = np.std(xvals3nm)/math.sqrt(3)
Std4nm = np.std(xvals4nm)/math.sqrt(3)
Std5nm = np.std(xvals5nm)/math.sqrt(3)
AllStd = [Std2nm,Std3nm,Std4nm,Std5nm]

C2nm = ParseMonInformation("/media/jje63/easystore/Multinano_C1_2/Dodecanethiol_C1/cluster11.dat")
C2nm1 =ParseMonInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano/Dodecanethiol_C1/cluster11.dat")
C2nm2 =ParseMonInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano_2/Dodecanethiol_C1/cluster11.dat")
C3nm =ParseMonInformation("/media/jje63/easystore/Bridges2/jennis/Bending_Carb/3nm_C1/cluster11.dat")
C3nm1 =ParseMonInformation("/media/jje63/easystore/Bridges2/jennis/Bending_Carb/3nm_C2/cluster11.dat")
C3nm2 =ParseMonInformation("/media/jje63/easystore/Bridges2/jennis/Bending_Carb/3nm_C3/cluster11.dat")
C4nm =ParseMonInformation("/media/jje63/easystore/Bridges2/jennis/Bending_Carb/4nm_C1/cluster11.dat")
C4nm1 =ParseMonInformation("/media/jje63/easystore/Bridges2/jennis/Bending_Carb/4nm_C2/cluster11.dat")
C4nm2 =ParseMonInformation("/media/jje63/easystore/Bridges2/jennis/Bending_Carb/4nm_C3/cluster11.dat")
C5nm =ParseMonInformation("/media/jje63/easystore/Bridges2/jennis/Bending_Carb/5nm_C1/cluster11.dat")
C5nm1 =ParseMonInformation("/media/jje63/easystore/Bridges2/jennis/Bending_Carb/5nm_C2/cluster11.dat")
C5nm2 =ParseMonInformation("/media/jje63/easystore/Bridges2/jennis/Bending_Carb/5nm_C3/cluster11.dat")


Cxvals2nm = np.array([np.mean(np.array(C2nm[1][20:])),np.mean(np.array(C2nm1[1][20:])),np.mean(np.array(C2nm2[1][20:]))])
Cxvals3nm = np.array([np.mean(np.array(C3nm[1][20:])),np.mean(np.array(C3nm1[1][20:])),np.mean(np.array(C3nm2[1][20:]))])
Cxvals4nm = np.array([np.mean(np.array(C4nm[1][20:])),np.mean(np.array(C4nm1[1][20:])),np.mean(np.array(C4nm2[1][20:]))])
Cxvals5nm = np.array([np.mean(np.array(C5nm[1][20:])),np.mean(np.array(C5nm1[1][20:])),np.mean(np.array(C5nm2[1][20:]))])


CAvg2nm = np.mean(Cxvals2nm)
CAvg3nm = np.mean(Cxvals3nm)
CAvg4nm = np.mean(Cxvals4nm)
CAvg5nm = np.mean(Cxvals5nm)
CAllAvg = [CAvg2nm,CAvg3nm,CAvg4nm,CAvg5nm]

CStd2nm = np.std(Cxvals2nm)/math.sqrt(3)
CStd3nm = np.std(Cxvals3nm)/math.sqrt(3)
CStd4nm = np.std(Cxvals4nm)/math.sqrt(3)
CStd5nm = np.std(Cxvals5nm)/math.sqrt(3)
CAllStd = [CStd2nm,CStd3nm,CStd4nm,CStd5nm]

figure , axs = plt.subplots(1, figsize=(8,6), sharex=True)
figure.tight_layout(pad=2)
axs.errorbar([2,3,4,5], AllAvg, yerr= AllStd,linestyle='dotted',linewidth=3, marker='^',markersize = 13,capsize=8,color="#BA6E6E",label="Charged Core")
#axs.errorbar([2,3,4,5], CAllAvg, yerr= CAllStd,linestyle='dotted',linewidth=3, marker='o',markersize = 13,capsize=8,color="#439FEF",label="Hydrophobic Core")
axs.set_ylabel('$<M_{f}>$',fontdict=font)
axs.set_xlabel('$N_{s}$ ($nm$)',fontdict=font)
plt.yticks(np.arange(0, 1.2, step=0.2))
#plt.legend(loc="upper right",bbox_to_anchor=(1.0, 1.0),fontsize='x-large')
plt.savefig("/media/jje63/easystore/Graphs/MonomerFraction_NanoparticleSizecharged.pdf",format='pdf',dpi=500, bbox_inches='tight')
"""

### Radius of gyration Ligand Length ###

"""
Oct = ParseRgyrInformation("/media/jje63/easystore/Octanethiol/radiusofgyrationcluster.dat")
Oct1 =ParseRgyrInformation("/media/jje63/easystore/Octanethiol_1/radiusofgyrationcluster.dat")
Oct2 =ParseRgyrInformation("/media/jje63/easystore/Octanethiol_2/radiusofgyrationcluster.dat")
Dod =ParseRgyrInformation("/media/jje63/My Passport/10np_membrane/radiusofgyrationcluster.dat")
Dod1 =ParseRgyrInformation("/media/jje63/easystore/NP_Concentration/10np_membrane/radiusofgyrationcluster.dat")
Dod2 =ParseRgyrInformation("/media/jje63/easystore/NP_Concentration/10np_membrane/radiusofgyrationcluster.dat")
Hex =ParseRgyrInformation("/media/jje63/easystore/Hexadecanethiol/radiusofgyrationcluster.dat")
Hex1 =ParseRgyrInformation("/media/jje63/easystore/Hexadecanethiol_1/radiusofgyrationcluster.dat")
Hex2 =ParseRgyrInformation("/media/jje63/easystore/Hexadecanethiol_2/radiusofgyrationcluster.dat")
Ico =ParseRgyrInformation("/media/jje63/easystore/Icosanethiol/radiusofgyrationcluster.dat")
Ico1 =ParseRgyrInformation("/media/jje63/easystore/Icosanethiol_1/radiusofgyrationcluster.dat")
Ico2 =ParseRgyrInformation("/media/jje63/easystore/Icosanethiol_2/radiusofgyrationcluster.dat")
Tetco =ParseRgyrInformation("/media/jje63/easystore/Bridges2/jennis/Tetracosanethiol/tetracosanethiol_1/radiusofgyrationcluster.dat")

xvalsOct = np.array([np.mean(Oct[3:])/math.sqrt(10),np.mean(Oct1[3:])/math.sqrt(10),np.mean(Oct2[3:])/math.sqrt(10)])
xvalsDod = np.array([np.mean(Dod[3:])/math.sqrt(10),np.mean(Dod1[3:])/math.sqrt(10),np.mean(Dod2[3:])/math.sqrt(10)])
xvalsHex = np.array([np.mean(Hex[3:])/math.sqrt(10),np.mean(Hex1[3:])/math.sqrt(10),np.mean(Hex2[3:])/math.sqrt(10)])
xvalsIco = np.array([np.mean(Ico[3:])/math.sqrt(10),np.mean(Ico1[3:])/math.sqrt(10),np.mean(Ico2[3:])/math.sqrt(10)])
xvalsTetco = np.array([np.mean(Tetco[3:])/math.sqrt(10)])

#print(xvalsHex)
AvgOct = np.mean(xvalsOct)
AvgDod = np.mean(xvalsDod)
AvgHex = np.mean(xvalsHex)
AvgIco = np.mean(xvalsIco)
AvgTetco = np.mean(xvalsTetco)
AllAvg = [AvgOct,AvgDod,AvgHex,AvgIco,AvgTetco]

StdOct = np.std(xvalsOct)/math.sqrt(3)
StdDod = np.std(xvalsDod)/math.sqrt(3)
StdHex = np.std(xvalsHex)/math.sqrt(3)
StdIco = np.std(xvalsIco)/math.sqrt(3)
StdTetco = np.std(xvalsTetco)/math.sqrt(1)
AllStd = [StdOct,StdDod,StdHex,StdIco,StdTetco]

#plt.errorbar([8,12,16,20], AllAvg, yerr= AllStd,linestyle='None', marker='^',markersize = 10,color="red")

COct = ParseRgyrInformation("/media/jje63/easystore/Multinano_C1_2/Octanethiol_C1/radiusofgyrationcluster.dat")
COct1 =ParseRgyrInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano/Octanethiol_P1/radiusofgyrationcluster.dat")
COct2 =ParseRgyrInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano_2/Octanethiol_P1/radiusofgyrationcluster.dat")
CDod =ParseRgyrInformation("/media/jje63/easystore/Multinano_C1_2/Dodecanethiol_C1/radiusofgyrationcluster.dat")
CDod1 =ParseRgyrInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano/Dodecanethiol_C1/radiusofgyrationcluster.dat")
CDod2 =ParseRgyrInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano_2/Dodecanethiol_C1/radiusofgyrationcluster.dat")
CHex =ParseRgyrInformation("/media/jje63/easystore/Multinano_C1_2/Hexadecanethiol_C1/radiusofgyrationcluster.dat")
CHex1 =ParseRgyrInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano/Hexadecanethiol_C1/radiusofgyrationcluster.dat")
CHex2 =ParseRgyrInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano_2/Hexadecanethiol_C1/radiusofgyrationcluster.dat")
CIco =ParseRgyrInformation("/media/jje63/easystore/Multinano_C1_2/Icotest/radiusofgyrationcluster.dat")
CIco1 =ParseRgyrInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano/Icosanethiol_C1/radiusofgyrationcluster.dat")
CIco2 =ParseRgyrInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano_2/Icosanethiol_C1/radiusofgyrationcluster.dat")
CTetco =ParseRgyrInformation("/media/jje63/easystore/Bridges2/jennis/Tetracosanethiol/tetracosanethiol_1C/radiusofgyrationcluster.dat")
  

CxvalsOct = np.array([np.mean(COct[3:])/math.sqrt(10),np.mean(COct1[3:])/math.sqrt(10),np.mean(COct2[3:])/math.sqrt(10)])
CxvalsDod = np.array([np.mean(CDod[3:])/math.sqrt(10),np.mean(CDod1[3:])/math.sqrt(10),np.mean(CDod2[3:])/math.sqrt(10)])
CxvalsHex = np.array([np.mean(CHex[3:])/math.sqrt(10),np.mean(CHex1[3:])/math.sqrt(10),np.mean(CHex2[3:])/math.sqrt(10)])
CxvalsIco = np.array([np.mean(CIco[3:])/math.sqrt(10),np.mean(CIco1[3:])/math.sqrt(10),np.mean(CIco2[3:])/math.sqrt(10)])
CxvalsTetco = np.array([np.mean(CTetco[3:])/math.sqrt(10)])

CAvgOct = np.mean(CxvalsOct)
CAvgDod = np.mean(CxvalsDod)
CAvgHex = np.mean(CxvalsHex)
CAvgIco = np.mean(CxvalsIco)
CAvgTetco = np.mean(CxvalsTetco)
CAllAvg = [CAvgOct,CAvgDod,CAvgHex,CAvgIco,CAvgTetco]


CStdOct = np.std(CxvalsOct)/math.sqrt(3)
CStdDod = np.std(CxvalsDod)/math.sqrt(3)
CStdHex = np.std(CxvalsHex)/math.sqrt(3)
CStdIco = np.std(CxvalsIco)/math.sqrt(3)
CStdTetco = np.std(CxvalsTetco)/math.sqrt(1)
CAllStd = [CStdOct,CStdDod,CStdHex,CStdIco,CStdTetco]

plt.errorbar([8,12,16,20,24], AllAvg, yerr= AllStd,linestyle='None', marker='^',markersize = 10,color="red",label="Charged Gold Core")
plt.errorbar([8,12,16,20,24], CAllAvg, yerr= CAllStd,linestyle='None', marker='o',markersize = 8,alpha=.5,color="blue",label="Hydrophobic Gold Core")
#plt.yticks(np.arange(0, 1.2, step=0.2))
plt.legend(loc="upper right",bbox_to_anchor=(1.35, 1.15))
"""
### Order Parameter Ligand length ###

"""
Oct =ParseOrdInformation("/media/jje63/easystore/Octanethiol/OrderPO.dat")
Oct1 =ParseOrdInformation("/media/jje63/easystore/Octanethiol_1/OrderPO.dat")
Oct2 =ParseOrdInformation("/media/jje63/easystore/Octanethiol_2/OrderPO.dat")
Dod =ParseOrdInformation("/media/jje63/easystore/NP_Concentration/10np_membrane_3/OrderPO.dat")
Dod1 =ParseOrdInformation("/media/jje63/easystore/NP_Concentration/10np_membrane_4/OrderPO.dat")
Dod2 =ParseOrdInformation("/media/jje63/easystore/NP_Concentration/10np_membrane_5/OrderPO.dat")
#Dodx =ParseOrdInformation("/media/jje63/easystore/NP_Concentration/10np_membrane_5/OrderPO.dat")
Hex =ParseOrdInformation("/media/jje63/easystore/Hexadecanethiol/OrderPO.dat")
Hex1 =ParseOrdInformation("/media/jje63/easystore/Hexadecanethiol_1/OrderPO.dat")
Hex2 =ParseOrdInformation("/media/jje63/easystore/Hexadecanethiol_2/OrderPO.dat")
Ico =ParseOrdInformation("/media/jje63/easystore/Icosanethiol/OrderPO.dat")
Ico1 =ParseOrdInformation("/media/jje63/easystore/Icosanethiol_1/OrderPO.dat")
Ico2 =ParseOrdInformation("/media/jje63/easystore/Icosanethiol_2/OrderPO.dat")
Tetco =ParseOrdInformation("/media/jje63/easystore/Bridges2/jennis/Tetracosanethiol/tetracosanethiol_1/OrderPO.dat")
Tetco1 =ParseOrdInformation("/media/jje63/easystore/Bridges2/jennis/Tetracosanethiol/tetracosanethiol_2/OrderPO.dat")
Tetco2 =ParseOrdInformation("/media/jje63/easystore/Bridges2/jennis/Tetracosanethiol/tetracosanethiol_3/OrderPO.dat")

xvalsOct=np.array([np.mean(np.array(Oct[1:])),np.mean(np.array(Oct1[1:])),np.mean(np.array(Oct2[1:]))])
xvalsDod=np.array([np.mean(np.array(Dod[1:])),np.mean(np.array(Dod1[1:])),np.mean(np.array(Dod2[1:]))])
#xvalsDod=np.array([np.mean(np.array(Dodx[1:]))])
xvalsHex=np.array([np.mean(np.array(Hex[1:])),np.mean(np.array(Hex1[1:])),np.mean(np.array(Hex2[1:]))])
xvalsIco=np.array([np.mean(np.array(Ico[1:])),np.mean(np.array(Ico1[1:])),np.mean(np.array(Ico2[1:]))])
xvalsTetco=np.array([np.mean(np.array(Tetco[1:])),np.mean(np.array(Tetco1[1:])),np.mean(np.array(Tetco2[1:]))])

AvgOct = np.mean(xvalsOct)
AvgDod = np.mean(xvalsDod)
AvgHex = np.mean(xvalsHex)
AvgIco = np.mean(xvalsIco)
AvgTetco = np.mean(xvalsTetco)
AllAvgOP = [AvgOct,AvgDod,AvgHex,AvgIco,AvgTetco]

StdOct = np.std(xvalsOct)/math.sqrt(3)
StdDod = np.std(xvalsDod)/math.sqrt(3)
StdHex = np.std(xvalsHex)/math.sqrt(3)
StdIco = np.std(xvalsIco)/math.sqrt(3)
StdTetco = np.std(xvalsTetco)/math.sqrt(3)
AllStd = [StdOct,StdDod,StdHex,StdIco,StdTetco]

COct =ParseOrdInformation("/media/jje63/easystore/Multinano_C1_2/Octanethiol_C1/OrderPO.dat")
COct1 =ParseOrdInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano/Octanethiol_P1/OrderPO.dat")
COct2 =ParseOrdInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano_2/Octanethiol_P1/OrderPO.dat")
CDod =ParseOrdInformation("/media/jje63/easystore/Multinano_C1_2/Dodecanethiol_C1/OrderPO.dat")
CDod1 =ParseOrdInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano/Dodecanethiol_C1/OrderPO.dat")
CDod2 =ParseOrdInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano_2/Dodecanethiol_C1/OrderPO.dat")
CHex =ParseOrdInformation("/media/jje63/easystore/Multinano_C1_2/Hexadecanethiol_C1/OrderPO.dat")
CHex1 =ParseOrdInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano/Hexadecanethiol_C1/OrderPO.dat")
CHex2 =ParseOrdInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano_2/Hexadecanethiol_C1/OrderPO.dat")
CIco =ParseOrdInformation("/media/jje63/easystore/Multinano_C1_2/Icotest/OrderPO.dat")
CIco1 =ParseOrdInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano/Icosanethiol_C1/OrderPO.dat")
CIco2 =ParseOrdInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano_2/Icosanethiol_C1/OrderPO.dat")
CTetco =ParseOrdInformation("/media/jje63/easystore/Bridges2/jennis/Tetracosanethiol/tetracosanethiol_1C/OrderPO.dat")
CTetco1 =ParseOrdInformation("/media/jje63/easystore/Bridges2/jennis/Tetracosanethiol/tetracosanethiol_2C/OrderPO.dat")
CTetco2 =ParseOrdInformation("/media/jje63/easystore/Bridges2/jennis/Tetracosanethiol/tetracosanethiol_3C/OrderPO.dat")


CxvalsOct=np.array([np.mean(np.array(COct[1:])),np.mean(np.array(COct1[1:])),np.mean(np.array(COct2[1:]))])
CxvalsDod=np.array([np.mean(np.array(CDod[1:])),np.mean(np.array(CDod1[1:])),np.mean(np.array(CDod2[1:]))])
CxvalsHex=np.array([np.mean(np.array(CHex[1:])),np.mean(np.array(CHex1[1:])),np.mean(np.array(CHex2[1:]))])
CxvalsIco=np.array([np.mean(np.array(CIco[1:])),np.mean(np.array(CIco1[1:])),np.mean(np.array(CIco2[1:]))])
CxvalsTetco=np.array([np.mean(np.array(CTetco[1:])-.005),np.mean(np.array(CTetco1[1:])-.005),np.mean(np.array(CTetco2[1:])-.005)])

CAvgOct = np.mean(CxvalsOct)
CAvgDod = np.mean(CxvalsDod)
CAvgHex = np.mean(CxvalsHex)
CAvgIco = np.mean(CxvalsIco)
CAvgTetco = np.mean(CxvalsTetco)
CAllAvgOP = [CAvgOct,CAvgDod,CAvgHex,CAvgIco,CAvgTetco]

CStdOct = np.std(CxvalsOct)/math.sqrt(3)
CStdDod = np.std(CxvalsDod)/math.sqrt(3)
CStdHex = np.std(CxvalsHex)/math.sqrt(3)
CStdIco = np.std(CxvalsIco)/math.sqrt(3)
CStdTetco = np.std(CxvalsTetco)/math.sqrt(3)
CAllStd = [CStdOct,CStdDod,CStdHex,CStdIco,CStdTetco]



#plt.errorbar([8,12,16,20,24],AllAvg,yerr= AllStd,linewidth=3,linestyle='dotted',marker='^',markersize = 13,capsize=8,color="#BA6E6E",label="Charged Core")
#plt.errorbar([8,12,16,20,24], CAllAvg, yerr= CAllStd,linewidth=3,linestyle='dotted', marker='o',markersize = 13,capsize=8,color="#439FEF",label="Hydrophobic Core")

#plt.ylabel(r'$\langle S \rangle$',fontdict=font)
#plt.xlabel('$L_{l}$',fontdict=font)
#plt.yticks(np.arange(.250, .260, step=0.002))
#plt.legend(loc="upper right",bbox_to_anchor=(1.0, 1.0))
#plt.savefig("/media/jje63/easystore/Graphs/OrderParameter_LigandLengthcharged.pdf",format='pdf',dpi=500, bbox_inches='tight')


figure , axs = plt.subplots(1, figsize=(8,6), sharex=True)
figure.tight_layout(pad=2)
axs.scatter(AllAvgOP, AllAvgAgg, s=80, marker='^',color="#BA6E6E",label="Charged")
axs.scatter(CAllAvgOP, CAllAvgAgg, s=80, marker='o',color="#439FEF",label="Hydrophobic")
#axs.set_yticks(np.arange(0, 1.2, step=0.2))
#axs.set_yticklabels(["$0.0$","$0.2$","$0.4$","$0.6$","$0.8$","$1.0$"],fontdict=font2)
axs.set_ylabel(r'$\langle F_{a} \rangle$',fontdict=font)
axs.set_xlabel(r'$\langle S \rangle$',fontdict=font)
axs.legend(loc="upper right",bbox_to_anchor=(1.0, 1.0))
plt.savefig("/media/jje63/easystore/Graphs/OrderParameter_v_Faggregate.pdf",format='pdf',dpi=500, bbox_inches='tight')
"""


### Order Parameter Ligand Length Single NP ###

"""
BareAvg =ParseOrdInformation("/media/jje63/easystore/POPCMembrane/TestOrd.dat")
#Dod1Avg =ParseOrdInformation("/home/jje63/Documents/SingleNP_Sim/ChargeSim/Dodecanethiol/TestOrd.dat")
#Hex1Avg =ParseOrdInformation("/home/jje63/Documents/SingleNP_Sim/ChargeSim/Hexadecanethiol/TestOrd.dat")
#Ico1Avg =ParseOrdInformation("/home/jje63/Documents/SingleNP_Sim/ChargeSim/Icosanethiol/TestOrd.dat")

xvalsbare=np.array(BareAvg)
xvalsbare=(np.repeat(np.mean(xvalsbare), 7))
#xvalsDod=np.array(Dod1Avg)
#xvalsHex=np.array(Hex1Avg)
#xvalsIco=np.array(Ico1Avg)

#CDod1Avg =ParseOrdInformation("/media/jje63/easystore/SingleNP_HydPho_sys/Dodecanethiol/TestorderB.dat")
#CHex1Avg =ParseOrdInformation("/media/jje63/easystore/SingleNP_HydPho_sys/Hexadecanethiol/TestorderB.dat")
#CIco1Avg =ParseOrdInformation("/media/jje63/easystore/SingleNP_HydPho_sys/Icosanethiol/TestorderB.dat")

#CxvalsDod=np.array(CDod1Avg[:-2])
#CxvalsHex=np.array(CHex1Avg[:-2])
#CxvalsIco=np.array(CIco1Avg[:-2])

OctAvgQa =ParseOrdInformation("/media/jje63/easystore1/SingleNP_Qa/Octanethiol/TestOrd.dat")
TetcoAvgQa =ParseOrdInformation("/media/jje63/easystore1/SingleNP_Qa/Tetracosanethiol/TestOrd.dat")
xvalsOctQa=np.array(OctAvgQa)
xvalsTetcoQa=np.array(TetcoAvgQa)

OctAvgC1 =ParseOrdInformation("/media/jje63/easystore1/SingleNP_C1/Octanethiol/TestOrd.dat")
TetcoAvgC1 =ParseOrdInformation("/media/jje63/easystore1/SingleNP_C1/Tetracosanethiol/TestOrd.dat")
xvalsOctC1=np.array(OctAvgC1)
xvalsTetcoC1=np.array(TetcoAvgC1)



OctAvgP5 =ParseOrdInformation("/media/jje63/easystore1/SingleNP_P5/Octanethiol/TestOrd.dat")
DodAvgP5 =ParseOrdInformation("/media/jje63/easystore1/SingleNP_P5/Dodecanethiol/TestOrd.dat")
HexAvgP5 =ParseOrdInformation("/media/jje63/easystore1/SingleNP_P5/Hexadecanethiol/TestOrd.dat")
IcoAvgP5 =ParseOrdInformation("/media/jje63/easystore1/SingleNP_P5/Icosanethiol/TestOrd.dat")
TetcoAvgP5 =ParseOrdInformation("/media/jje63/easystore1/SingleNP_P5/Tetracosanethiol/TestOrd.dat")
xvalsOctP5=np.array(OctAvgP5)
xvalsDodP5=np.array(DodAvgP5)
xvalsHexP5=np.array(HexAvgP5)
xvalsIcoP5=np.array(IcoAvgP5)
xvalsTetcoP5=np.array(TetcoAvgP5)

OctAvgC5 =ParseOrdInformation("/media/jje63/easystore1/SingleNP_C5/Octanethiol/TestOrd.dat")
DodAvgC5 =ParseOrdInformation("/media/jje63/easystore1/SingleNP_C5/Dodecanethiol/TestOrd.dat")
HexAvgC5 =ParseOrdInformation("/media/jje63/easystore1/SingleNP_C5/Hexadecanethiol/TestOrd.dat")
IcoAvgC5 =ParseOrdInformation("/media/jje63/easystore1/SingleNP_C5/Icosanethiol/TestOrd.dat")
TetcoAvgC5 =ParseOrdInformation("/media/jje63/easystore1/SingleNP_C5/Tetracosanethiol/TestOrd.dat")
xvalsOctC5=np.array(OctAvgC5)
xvalsDodC5=np.array(DodAvgC5)
xvalsHexC5=np.array(HexAvgC5)
xvalsIcoC5=np.array(IcoAvgC5)
xvalsTetcoC5=np.array(TetcoAvgC5)

OctAvgSS =ParseOrdInformation("/media/jje63/easystore1/SingleNP_SS/Octanethiol/TestOrd.dat")
TetcoAvgSS =ParseOrdInformation("/media/jje63/easystore1/SingleNP_SS/Tetracosanethiol/TestOrd.dat")
xvalsOctSS=np.array(OctAvgSS)
xvalsTetcoSS=np.array(TetcoAvgSS)

OctAvgP1 =ParseOrdInformation("/media/jje63/easystore/SingleNP_Polar_Sys/Octanethiol/TestOrd.dat")
xvalsOctP1=np.array(OctAvgP1)


figure , axs = plt.subplots(2,2, figsize=(10,6), sharey=True)
#figure , axs = plt.subplots(1, figsize=(8,6), sharex=True, sharey=True)
figure.tight_layout(pad=2)

#axs.plot([10,20,30,40,50,60],xvalsbare,linewidth=2,linestyle="dashed",marker='o',markersize = 10,color="grey",label="Hydrophobic Bare")
#axs.plot([10,20,30,40,50,60],xvalsDod,linewidth=1,marker='^',markersize = 10,color="#D3BEA7",label="Charged Dodecanethiol")
#axs.plot([10,20,30,40,50,60],xvalsHex,linewidth=2,marker='^',markersize = 10,color="#CBA394",label="Charged Hexadecanethiol")
#axs.plot([10,20,30,40,50,60],xvalsIco,linewidth=2,marker='^',markersize = 10,color="#C28981",label="Charged Icosanethiol")

#axs.plot([10,20,30,40,50,60],xvalsbare,linewidth=2,linestyle="dashed",marker='o',markersize = 10,color="grey",label="Hydrophobic Bare")
#axs.plot([10,20,30,40,50,60],CxvalsDod,linewidth=1,marker='o',markersize = 10,color="#8F9AC7",label="Hydrophobic Dodecanethiol")
#axs.plot([10,20,30,40,50,60],CxvalsHex,linewidth=2,marker='o',markersize = 10,color="#6668C7",label="Hydrophobic Hexadecanethiol")
#axs.plot([10,20,30,40,50,60],CxvalsIco,linewidth=2,marker='o',markersize = 10,color="#3C35C7",label="Hydrophobic Icosanethiol")


#axs.plot(np.array([5,10,15,20,25,30,35,40,45,50,55,60,65,70]),xvalsOctC5[0:14],linewidth=2,marker='^',markersize = 10,color="#DBD8BA",label="Octanethiol C5")
#axs.plot(np.array([5,10,15,20,25,30,35,40,45,50,55,60,65,70]),xvalsDodC5[0:14],linewidth=2,marker='^',markersize = 10,label="Dodecanethiol C5")
#axs.plot(np.array([5,10,15,20,25,30,35,40,45,50,55,60,65,70]),xvalsHexC5[0:14],linewidth=2,marker='^',markersize = 10,label="Hexadecanethiol C5")
#axs.plot(np.array([5,10,15,20,25,30,35,40,45,50,55,60,65,70]),xvalsIcoC5[0:14],linewidth=2,marker='^',markersize = 10,label="Icosanethiol C5")
#axs.plot(np.array([5,10,15,20,25,30,35,40,45,50,55,60,65,70]),xvalsTetcoC5[0:14],linewidth=2,marker='^',markersize = 10,color="#BA6E6E",label="Tetracosanethiol C5")


#axs.plot(np.array([5,10,15,20,25,30,35,40,45,50,55,60,65,70]),xvalsOctP5[0:14],linewidth=2,marker='^',markersize = 10,color="#DBD8BA",label="Octanethiol P5")
#axs.plot(np.array([5,10,15,20,25,30,35,40,45,50,55,60,65,70]),xvalsDodP5[0:14],linewidth=2,marker='^',markersize = 10,label="Dodecanethiol P5")
#axs.plot(np.array([5,10,15,20,25,30,35,40,45,50,55,60,65,70]),xvalsHexP5[0:14],linewidth=2,marker='^',markersize = 10,label="Hexadecanethiol P5")
#axs.plot(np.array([5,10,15,20,25,30,35,40,45,50,55,60,65,70]),xvalsIcoP5[0:14],linewidth=2,marker='^',markersize = 10,label="Icosanethiol P5")
#axs.plot(np.array([5,10,15,20,25,30,35,40,45,50,55,60,65,70]),xvalsTetcoP5[0:14],linewidth=2,marker='^',markersize = 10,color="#BA6E6E",label="Tetracosanethiol P5")


axs[0,0].plot([10,20,30,40,50,60,70],xvalsOctC5[:-1],linewidth=2,marker='o',markersize = 10,color="#B8CDC7",label="Octanethiol C5")
axs[0,0].plot([10,20,30,40,50,60,70],xvalsDodC5[:-1],linewidth=2,marker='o',markersize = 10,color="#8F9AC7",label="Dodecanethiol C5")
axs[0,0].plot([10,20,30,40,50,60,70],xvalsHexC5[:-1],linewidth=2,marker='o',markersize = 10,color="#6668C7",label="Hexadecanethiol C5")
axs[0,0].plot([10,20,30,40,50,60,70],xvalsIcoC5[:-1],linewidth=2,marker='o',markersize = 10,color="#3C35C7",label="Icosanethiol C5")
axs[0,0].plot([10,20,30,40,50,60,70],xvalsTetcoC5[:-1],linewidth=2,marker='o',markersize = 10,color="#1302C7",label="Tetracosanethiol C5")
axs[0,0].plot([10,20,30,40,50,60,70],xvalsbare,linewidth=2,linestyle="dashed",color="grey",label="Bare")

axs[1,0].plot([10,20,30,40,50,60,70],xvalsOctP5[:-1],linewidth=2,marker='o',markersize = 10,color="#EFD7D7",label="Octanethiol C5")
axs[1,0].plot([10,20,30,40,50,60,70],xvalsDodP5[:-1],linewidth=2,marker='o',markersize = 10,color="#DFA2A2",label="Dodecanethiol C5")
axs[1,0].plot([10,20,30,40,50,60,70],xvalsHexP5[:-1],linewidth=2,marker='o',markersize = 10,color="#CF6D6D",label="Hexadecanethiol C5")
axs[1,0].plot([10,20,30,40,50,60,70],xvalsIcoP5[:-1],linewidth=2,marker='o',markersize = 10,color="#BF3838",label="Icosanethiol C5")
axs[1,0].plot([10,20,30,40,50,60,70],xvalsTetcoP5[:-1],linewidth=2,marker='o',markersize = 10,color="#AF0303",label="Tetracosanethiol C5")
axs[1,0].plot([10,20,30,40,50,60,70],xvalsbare,linewidth=2,linestyle="dashed",color="grey",label="Bare")

axs[0,1].plot([8,12,16,20,24],[np.mean(xvalsOctC5[0:2]),np.mean(xvalsDodC5[0:2]),np.mean(xvalsHexC5[0:2]),np.mean(xvalsIcoC5[0:2]),np.mean(xvalsTetcoC5[0:2])],color="blue",linewidth=2,marker='^',markersize=10,label="C5")
axs[0,1].plot([8,12,16,20,24],xvalsbare[:-2],linewidth=2,linestyle="dashed",color="grey",label="Bare")

axs[1,1].plot([8,12,16,20,24],[np.mean(xvalsOctP5[0:2]),np.mean(xvalsDodP5[0:2]),np.mean(xvalsHexP5[0:2]),np.mean(xvalsIcoP5[0:2]),np.mean(xvalsTetcoP5[0:2])],color="red",linewidth=2,marker='^',markersize=10,label="P5")
axs[1,1].plot([8,12,16,20,24],xvalsbare[:-2],linewidth=2,linestyle="dashed",color="grey",label="Bare")

#axs.scatter(["C1","C5","SS","P5","Qa"],[xvalsOctC1[0],xvalsOctC5[0],xvalsOctSS[0],xvalsOctP5[0],xvalsOctQa[0]],linewidth=2,marker='^',s=100,label="Octanethiol")
#axs.scatter(["C1","C5","SS","P5","Qa"],[xvalsTetcoC1[0],xvalsTetcoC5[0],xvalsTetcoSS[0],xvalsTetcoP5[0],xvalsTetcoQa[0]],linewidth=2,s=100,marker='^',label="Tetracosanethiol")

#axs.scatter(["C1","C5","SS","P5","Qa"],[np.mean(xvalsOctC1[0:2]),np.mean(xvalsOctC5[0:2]),np.mean(xvalsOctSS[0:2]),np.mean(xvalsOctP5[0:2]),np.mean(xvalsOctQa[0:2])],linewidth=2,s=100,marker='^',label="Octanethiol")
#axs.scatter(["C1","C5","SS","P5","Qa"],[np.mean(xvalsTetcoC1[0:2]),np.mean(xvalsTetcoC5[0:2]),np.mean(xvalsTetcoSS[0:2]),np.mean(xvalsTetcoP5[0:2]),np.mean(xvalsTetcoQa[0:2])],linewidth=2,s=100,marker='^',label="Tetracosanethiol")


#axs.legend(loc="upper right",bbox_to_anchor=(1.0, 1.0),fontsize='small')
#axs.set_yticks(np.arange(.26, .34, step=0.02))
axs[0,0].set_yticks(np.arange(.160,.325, step=0.04))
#axs[2,0].set_yticks(np.arange(.22, .34, step=0.02))
figure.text(0.28, 0.00, '$d_{s}$', ha='center',fontdict=font)
figure.text(0.78, 0.00, '$l_{l}$', ha='center',fontdict=font)
figure.text(-0.04, 0.5, r'$\langle S \rangle$', va='center', rotation='vertical',fontdict=font)
#plt.xlabel("Distance ($nm$)",fontdict=font)
#plt.ylabel("Bond Order Parameter",fontdict=font)
plt.savefig("/media/jje63/easystore1/Graphs/SingleNPOrderCore.pdf",format='pdf',dpi=500, bbox_inches='tight')
#plt.plot([8,12,16,20], CAllAvg,linestyle='None', marker='o',markersize = 8,alpha=.5,color="blue",label="Hydrophobic Gold Core")
"""


### SASA Test ###

## Polar##

"""
#BareSASA = ParseSASAInformation("/home/jje63/Documents/SingleNP_Sim/ChargeSim/Bare_NP")
ButSASA = ParseSASAInformation("/media/jje63/easystore/SingleNP_P5_2/Butanethiol")
OctSASA = ParseSASAInformation("/media/jje63/easystore/SingleNP_P5_2/Octanethiol")
DodSASA = ParseSASAInformation("/media/jje63/easystore/SingleNP_P5_2/Dodecanethiol")
HexSASA = ParseSASAInformation("/media/jje63/easystore/SingleNP_P5_2/Hexadecanethiol")
IcoSASA = ParseSASAInformation("/media/jje63/easystore/SingleNP_P5_2/Icosanethiol")
TetSASA = ParseSASAInformation("/media/jje63/easystore/SingleNP_P5_2/Tetracosanethiol")

ButSASA2 = ParseSASAInformation("/media/jje63/easystore/SingleNP_P5_3/Butanethiol")
OctSASA2 = ParseSASAInformation("/media/jje63/easystore/SingleNP_P5_3/Octanethiol")
DodSASA2 = ParseSASAInformation("/media/jje63/easystore/SingleNP_P5_3/Dodecanethiol")
HexSASA2 = ParseSASAInformation("/media/jje63/easystore/SingleNP_P5_3/Hexadecanethiol")
IcoSASA2 = ParseSASAInformation("/media/jje63/easystore/SingleNP_P5_3/Icosanethiol")
TetSASA2 = ParseSASAInformation("/media/jje63/easystore/SingleNP_P5_3/Tetracosanethiol")

ButSASA3 = ParseSASAInformation("/media/jje63/easystore/SingleNP_P5_4/Butanethiol")
OctSASA3 = ParseSASAInformation("/media/jje63/easystore/SingleNP_P5_4/Octanethiol")
DodSASA3 = ParseSASAInformation("/media/jje63/easystore/SingleNP_P5_4/Dodecanethiol")
HexSASA3 = ParseSASAInformation("/media/jje63/easystore/SingleNP_P5_4/Hexadecanethiol")
IcoSASA3 = ParseSASAInformation("/media/jje63/easystore/SingleNP_P5_4/Icosanethiol")
TetSASA3 = ParseSASAInformation("/media/jje63/easystore/SingleNP_P5_4/Tetracosanethiol")
#print(BareSASA)

#print(OctSASA['NP1'][1])
#plt.plot(np.arange(0,len(OctSASA['NP1'][1])),medfilt(OctSASA['NP1'][1], 15)) 
#plt.plot(np.arange(0,len(ButSASA['NP1'][1])),medfilt(ButSASA['NP1'][1], 15))
#plt.plot(np.arange(0,len(DodSASA['NP1'][1])),medfilt(DodSASA['NP1'][1], 15))
#plt.plot(np.arange(0,len(HexSASA['NP1'][1])),medfilt(HexSASA['NP1'][1], 15))
#plt.plot(np.arange(0,len(IcoSASA['NP1'][1])),medfilt(IcoSASA['NP1'][1], 15))

#AvgBare = AverageSASA(BareSASA)

AvgOctW = np.average(OctSASA['NP1'][1])
AvgDodW = np.average(DodSASA['NP1'][1])
AvgHexW = np.average(HexSASA['NP1'][1])
AvgIcoW = np.average(IcoSASA['NP1'][1])
AvgTetW = np.average(TetSASA['NP1'][1])


AvgOct2W = np.average(OctSASA2['NP1'][1])
AvgDod2W = np.average(DodSASA2['NP1'][1])
AvgHex2W = np.average(HexSASA2['NP1'][1])
AvgIco2W = np.average(IcoSASA2['NP1'][1])
AvgTet2W = np.average(TetSASA2['NP1'][1])


AvgOct3W = np.average(OctSASA3['NP1'][1])
AvgDod3W = np.average(DodSASA3['NP1'][1])
AvgHex3W = np.average(HexSASA3['NP1'][1])
AvgIco3W = np.average(IcoSASA3['NP1'][1])
AvgTet3W = np.average(TetSASA3['NP1'][1])



AllAvgOct = np.average([AvgOctW,AvgOct2W,AvgOct3W])
AllstdOct = np.std([AvgOctW,AvgOct2W,AvgOct3W])/math.sqrt(3)
AllAvgDod = np.average([AvgDodW,AvgDod2W,AvgDod3W])
AllstdDod = np.std([AvgDodW,AvgDod2W,AvgDod3W])/math.sqrt(3)
AllAvgHex = np.average([AvgHexW,AvgHex2W,AvgHex3W])
AllstdHex = np.std([AvgHexW,AvgHex2W,AvgHex3W])/math.sqrt(3)
AllAvgIco = np.average([AvgIcoW,AvgIco2W,AvgIco3W])
AllstdIco = np.std([AvgIcoW,AvgIco2W,AvgIco3W])/math.sqrt(3)
AllAvgTet = np.average([AvgTetW,AvgTet2W,AvgTet3W])
AllstdTet = np.std([AvgTetW,AvgTet2W,AvgTet3W])/math.sqrt(3)

AvgAll = [AllAvgOct, AllAvgDod, AllAvgHex, AllAvgIco, AllAvgTet]
AllSTD = [AllstdOct, AllstdDod, AllstdHex, AllstdIco, AllstdTet]


AvgOctL = np.average(OctSASA['NP2'][1])
AvgDodL = np.average(DodSASA['NP2'][1])
AvgHexL = np.average(HexSASA['NP2'][1])
AvgIcoL = np.average(IcoSASA['NP2'][1])
AvgTetL = np.average(TetSASA['NP2'][1])


AvgOct2L = np.average(OctSASA2['NP2'][1])
AvgDod2L = np.average(DodSASA2['NP2'][1])
AvgHex2L = np.average(HexSASA2['NP2'][1])
AvgIco2L = np.average(IcoSASA2['NP2'][1])
AvgTet2L = np.average(TetSASA2['NP2'][1])


AvgOct3L = np.average(OctSASA3['NP2'][1])
AvgDod3L = np.average(DodSASA3['NP2'][1])
AvgHex3L = np.average(HexSASA3['NP2'][1])
AvgIco3L = np.average(IcoSASA3['NP2'][1])
AvgTet3L = np.average(TetSASA3['NP2'][1])



AllAvgOct2 = np.average([AvgOctL,AvgOct2L,AvgOct3L])
AllstdOct2 = np.std([AvgOctL,AvgOct2L,AvgOct3L])/math.sqrt(3)
AllAvgDod2 = np.average([AvgDodL,AvgDod2L,AvgDod3L])
AllstdDod2 = np.std([AvgDodL,AvgDod2L,AvgDod3L])/math.sqrt(3)
AllAvgHex2 = np.average([AvgHexL,AvgHex2L,AvgHex3L])
AllstdHex2 = np.std([AvgHexL,AvgHex2L,AvgHex3L])/math.sqrt(3)
AllAvgIco2 = np.average([AvgIcoL,AvgIco2L,AvgIco3L])
AllstdIco2 = np.std([AvgIcoL,AvgIco2L,AvgIco3L])/math.sqrt(3)
AllAvgTet2 = np.average([AvgTetL,AvgTet2L,AvgTet3L])
AllstdTet2 = np.std([AvgTetL,AvgTet2L,AvgTet3L])/math.sqrt(3)

AvgAll2 = [AllAvgOct2, AllAvgDod2, AllAvgHex2, AllAvgIco2, AllAvgTet2]
AllSTD2 = [AllstdOct2, AllstdDod2, AllstdHex2, AllstdIco2, AllstdTet2]


## Hydrophobic ##

#ButSASAC = ParseSASAInformation("/media/jje63/easystore/SingleNP_C5/Butanethiol")
OctSASAC = ParseSASAInformation("/media/jje63/easystore/SingleNP_C5/Octanethiol")
DodSASAC = ParseSASAInformation("/media/jje63/easystore/SingleNP_C5/Dodecanethiol")
HexSASAC = ParseSASAInformation("/media/jje63/easystore/SingleNP_C5/Hexadecanethiol")
IcoSASAC = ParseSASAInformation("/media/jje63/easystore/SingleNP_C5/Icosanethiol")
TetSASAC = ParseSASAInformation("/media/jje63/easystore/SingleNP_C5/Tetracosanethiol")

OctSASAC2 = ParseSASAInformation("/media/jje63/easystore/singleNP_C5_2/Octanethiol")
DodSASAC2 = ParseSASAInformation("/media/jje63/easystore/singleNP_C5_2/Dodecanethiol")
HexSASAC2 = ParseSASAInformation("/media/jje63/easystore/singleNP_C5_2/Hexadecanethiol")
IcoSASAC2 = ParseSASAInformation("/media/jje63/easystore/singleNP_C5_2/Icosanethiol")
TetSASAC2 = ParseSASAInformation("/media/jje63/easystore/singleNP_C5_2/Tetracosanethiol")

OctSASAC3 = ParseSASAInformation("/media/jje63/easystore/singleNP_C5_3/Octanethiol")
DodSASAC3 = ParseSASAInformation("/media/jje63/easystore/singleNP_C5_3/Dodecanethiol")
HexSASAC3 = ParseSASAInformation("/media/jje63/easystore/singleNP_C5_3/Hexadecanethiol")
IcoSASAC3 = ParseSASAInformation("/media/jje63/easystore/singleNP_C5_3/Icosanethiol")
TetSASAC3 = ParseSASAInformation("/media/jje63/easystore/singleNP_C5_3/Tetracosanethiol")

#AvgButC = AverageSASA(ButSASAC)
AvgOctCW = np.average(OctSASAC['NP1'][1])
AvgDodCW = np.average(DodSASAC['NP1'][1])
AvgHexCW = np.average(HexSASAC['NP1'][1])
AvgIcoCW = np.average(IcoSASAC['NP1'][1])
AvgTetCW = np.average(TetSASAC['NP1'][1])

AvgOctC2W = np.average(OctSASAC2['NP1'][1])
AvgDodC2W = np.average(DodSASAC2['NP1'][1])
AvgHexC2W = np.average(HexSASAC2['NP1'][1])
AvgIcoC2W = np.average(IcoSASAC2['NP1'][1])
AvgTetC2W = np.average(TetSASAC2['NP1'][1])

AvgOctC3W = np.average(OctSASAC3['NP1'][1])
AvgDodC3W = np.average(DodSASAC3['NP1'][1])
AvgHexC3W = np.average(HexSASAC3['NP1'][1])
AvgIcoC3W = np.average(IcoSASAC3['NP1'][1])
AvgTetC3W = np.average(TetSASAC3['NP1'][1])

OctAVGC = np.average([AvgOctCW,AvgOctC2W,AvgOctC3W])
stdOctC = np.std([AvgOctCW,AvgOctC2W,AvgOctC3W])/math.sqrt(3)
DodAVGC = np.average([AvgDodCW,AvgDodC2W,AvgDodC3W])
stdDodC = np.std([AvgDodCW,AvgDodC2W,AvgDodC3W])/math.sqrt(3)
HexAVGC = np.average([AvgHexCW,AvgHexC2W,AvgHexC3W]) 
stdHexC = np.std([AvgHexCW,AvgHexC2W,AvgHexC3W])/math.sqrt(3)
IcoAVGC = np.average([AvgIcoCW,AvgIcoC2W,AvgIcoC3W])
stdIcoC = np.std([AvgIcoCW,AvgIcoC2W,AvgIcoC3W])/math.sqrt(3)
TetAVGC = np.average([AvgTetCW,AvgTetC2W,AvgTetC3W])
stdTetC = np.std([AvgTetCW,AvgTetC2W,AvgTetC3W])/math.sqrt(3)

AllAvgC = [OctAVGC,DodAVGC, HexAVGC, IcoAVGC, TetAVGC]
AllSTDC = [stdOctC,stdDodC, stdHexC, stdIcoC, stdTetC]

AvgOctCL = np.average(OctSASAC['NP2'][1])
AvgDodCL = np.average(DodSASAC['NP2'][1])
AvgHexCL = np.average(HexSASAC['NP2'][1])
AvgIcoCL = np.average(IcoSASAC['NP2'][1])
AvgTetCL = np.average(TetSASAC['NP2'][1])

AvgOctC2L = np.average(OctSASAC2['NP2'][1])
AvgDodC2L = np.average(DodSASAC2['NP2'][1])
AvgHexC2L = np.average(HexSASAC2['NP2'][1])
AvgIcoC2L = np.average(IcoSASAC2['NP2'][1])
AvgTetC2L = np.average(TetSASAC2['NP2'][1])

AvgOctC3L = np.average(OctSASAC3['NP2'][1])
AvgDodC3L = np.average(DodSASAC3['NP2'][1])
AvgHexC3L = np.average(HexSASAC3['NP2'][1])
AvgIcoC3L = np.average(IcoSASAC3['NP2'][1])
AvgTetC3L = np.average(TetSASAC3['NP2'][1])

OctAVGC2 = np.average([AvgOctCL,AvgOctC2L,AvgOctC3L])
stdOctC2 = np.std([AvgOctCL,AvgOctC2L,AvgOctC3L])/math.sqrt(3)
DodAVGC2 = np.average([AvgDodCL,AvgDodC2L,AvgDodC3L])
stdDodC2 = np.std([AvgDodCL,AvgDodC2L,AvgDodC3L])/math.sqrt(3)
HexAVGC2 = np.average([AvgHexCL,AvgHexC2L,AvgHexC3L]) 
stdHexC2 = np.std([AvgHexCL,AvgHexC2L,AvgHexC3L])/math.sqrt(3)
IcoAVGC2 = np.average([AvgIcoCL,AvgIcoC2L,AvgIcoC3L])
stdIcoC2 = np.std([AvgIcoCL,AvgIcoC2L,AvgIcoC3L])/math.sqrt(3)
TetAVGC2 = np.average([AvgTetCL,AvgTetC2L,AvgTetC3L])
stdTetC2 = np.std([AvgTetCL,AvgTetC2L,AvgTetC3L])/math.sqrt(3)

AllAvgC2 = [OctAVGC2,DodAVGC2, HexAVGC2,IcoAVGC2,TetAVGC2]
AllSTDC2 = [stdOctC2,stdDodC2, stdHexC2, stdIcoC2, stdTetC2]
"""

"""
## Soft Sphere ##
OctSASAS = ParseSASAInformation("/media/jje63/easystore/singleNP_SS/Octanethiol")
DodSASAS = ParseSASAInformation("/media/jje63/easystore/singleNP_SS/Dodecanethiol")
HexSASAS = ParseSASAInformation("/media/jje63/easystore/singleNP_SS/Hexadecanethiol")
IcoSASAS = ParseSASAInformation("/media/jje63/easystore/singleNP_SS/Icosanethiol")
TetSASAS = ParseSASAInformation("/media/jje63/easystore/singleNP_SS/Tetracosanethiol")

OctSASAS2 = ParseSASAInformation("/media/jje63/easystore/singleNP_SS_2/Octanethiol")
DodSASAS2 = ParseSASAInformation("/media/jje63/easystore/singleNP_SS_2/Dodecanethiol")
HexSASAS2 = ParseSASAInformation("/media/jje63/easystore/singleNP_SS_2/Hexadecanethiol")
IcoSASAS2 = ParseSASAInformation("/media/jje63/easystore/singleNP_SS_2/Icosanethiol")
TetSASAS2 = ParseSASAInformation("/media/jje63/easystore/singleNP_SS_2/Tetracosanethiol")

OctSASAS3 = ParseSASAInformation("/media/jje63/easystore/singleNP_SS_3/Octanethiol")
DodSASAS3 = ParseSASAInformation("/media/jje63/easystore/singleNP_SS_3/Dodecanethiol")
HexSASAS3 = ParseSASAInformation("/media/jje63/easystore/singleNP_SS_3/Hexadecanethiol")
IcoSASAS3 = ParseSASAInformation("/media/jje63/easystore/singleNP_SS_3/Icosanethiol")
TetSASAS3 = ParseSASAInformation("/media/jje63/easystore/singleNP_SS_3/Tetracosanethiol")


AvgOctS = np.average(OctSASAS)
AvgDodS = np.average(DodSASAS)
AvgHexS = np.average(HexSASAS)
AvgIcoS = np.average(IcoSASAS)
AvgTetS = np.average(TetSASAS)

AvgOctS2 = np.average(OctSASAS2)
AvgDodS2 = np.average(DodSASAS2)
AvgHexS2 = np.average(HexSASAS2)
AvgIcoS2 = np.average(IcoSASAS2)
AvgTetS2 = np.average(TetSASAS2)

AvgOctS3 = np.average(OctSASAS3)
AvgDodS3 = np.average(DodSASAS3)
AvgHexS3 = np.average(HexSASAS3)
AvgIcoS3 = np.average(IcoSASAS3)
AvgTetS3 = AverageSASA(TetSASAS3)

OctAVGS = np.average([AvgOctS,AvgOctS2,AvgOctS3])
stdOctS = np.std([AvgOctS,AvgOctS2,AvgOctS3])
DodAVGS = np.average([AvgDodS,AvgDodS2,AvgDodS3])
stdDodS = np.std([AvgDodS,AvgDodS2,AvgDodS3])
HexAVGS = np.average([AvgHexS,AvgHexS2,AvgHexS3]) 
stdHexS = np.std([AvgHexS,AvgHexS2,AvgHexS3])
IcoAVGS = np.average([AvgIcoS,AvgIcoS2,AvgIcoS3])
stdIcoS = np.std([AvgIcoS,AvgIcoS2,AvgIcoS3])
TetAVGS = np.average([AvgTetS,AvgTetS2,AvgTetS3])
stdTetS = np.std([AvgTetS,AvgTetS2,AvgTetS3])

AllAvgS = [OctAVGS,DodAVGS,HexAVGS,IcoAVGS,TetAVGS]
AllSTDS = [stdOctS,stdDodS, stdHexS, stdIcoS, stdTetS]


figure, (ax, ax2) = plt.subplots(2, 1, figsize=(8,6), sharex=True)

ax.errorbar([2,3,4,5,6], AvgAll, yerr=AllSTD,linestyle='solid',color="#fc8900",label="Polar",markersize = 8,marker='^', capsize = 8)
#plt.errorbar([2,3,4,5,6], AvgAll2, yerr=AllSTD2,linestyle='solid',color="#fc8900",label="Polar",markersize = 8,marker='^', capsize = 8)
ax2.errorbar([2,3,4,5,6], AllAvgC, yerr=AllSTDC,linestyle='solid',color="#003dfc",label="Hydrophobic",alpha=0.5,markersize = 8,marker='o', capsize = 8)
#plt.errorbar([2,3,4,5,6], AllAvgC2, yerr=AllSTDC2,linestyle='solid',color="#003dfc",label="Hydrophobic",alpha=0.5,markersize = 8,marker='o', capsize = 8)
#plt.errorbar([8,12,16,20,24], AllAvgS,yerr=AllSTDS,linestyle='solid',color="grey",label="Soft Sphere",markersize = 8,marker='o', capsize = 8)
#plt.yticks(np.arange(4.5, 9.0 , 0.5))
#plt.yscale('log')

#["(8-10)","(12-14)","(16-18)","(20-22)","(24-26)"]

#ax.set_ylim(4, 9)  
#ax2.set_ylim(0.004,0.010)  

ax.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
#ax.xaxis.tick_top()
ax.tick_params(labeltop=False, bottom=False)  # don't put tick labels at the top
ax2.xaxis.tick_bottom()
d = .015  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
ax.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

#plt.xlabel("Ligand Length")
#plt.ylabel("Lipid ASA($nm^{2}$)")
figure.text(0.52, 0.03, 'Ligand Length', ha='center', va='center',fontsize=25)
figure.text(0.023, 0.5, 'Water Accesible Surface Area ($nm^{2}$)', ha='center', va='center', rotation='vertical',fontsize=18)
#plt.legend(loc="upper right")
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=15)

ax2.tick_params(axis='y', labelsize=15)
ax2.tick_params(axis='x', labelsize=15)

figure.legend(loc = 'upper right', bbox_to_anchor = (-.1, -.12, 1, 1),
           bbox_transform = plt.gcf().transFigure)
#COctSASA = ParseSASAInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano/Octanethiol_P1")
#CIcoSASA = ParseSASAInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano/Icosanethiol_C1")
plt.savefig("/media/jje63/easystore/Graphs/waterSASAposter.pdf",format='pdf',dpi=500, bbox_inches='tight')
"""

### SASA Coverage ###

"""
#OctSASA = ParseSASAInformation("/media/jje63/easystore/Octanethiol")
SASA100 = ParseSASAInformation("/media/jje63/easystore/Coverage/100Dodecanethiol")
SASA80 = ParseSASAInformation("/media/jje63/easystore/Coverage/80Dodecanethiol")
SASA70 = ParseSASAInformation("/media/jje63/easystore/Coverage/70Dodecanethiol")
SASA60 = ParseSASAInformation("/media/jje63/easystore/Coverage/60Dodecanethiol")
SASA40 = ParseSASAInformation("/media/jje63/easystore/Coverage/40Dodecanethiol")
SASA20 = ParseSASAInformation("/media/jje63/easystore/Coverage/20Dodecanethiol")

#AvgOct = AverageSASA(OctSASA)
Avg100 = AverageSASA(SASA100)
Avg80 = AverageSASA(SASA80)
Avg70 = AverageSASA(SASA70)
Avg60 = AverageSASA(SASA60)
Avg40 = AverageSASA(SASA40)
Avg20 = AverageSASA(SASA20)

AvgAll = [Avg20,Avg40,Avg60,Avg80,Avg100]
plt.plot([20,40,60,80,100],AvgAll,linestyle='dotted',marker='^',markersize = 10,color="orange",label="SASA")
plt.xlabel("Coverage(%)")
plt.ylabel("SASA($nm^{2}$)")
#plt.yticks(np.arange(325 , 360, step=5))
#plt.savefig("/media/jje63/easystore/Graphs/SASA_Coverage.pdf",format='pdf',dpi=500, bbox_inches='tight')
"""


### SASA Distance ###

"""
OctSS = ParseSASAInformation("/media/jje63/easystore/SingleNP_SS/Octanethiol")
OctQa = ParseSASAInformation("/media/jje63/easystore/SingleNP_Qa/Octanethiol")
OctP5 = ParseSASAInformation("/media/jje63/easystore/SingleNP_P5/Octanethiol")
OctC5 = ParseSASAInformation("/media/jje63/easystore/SingleNP_C5/Octanethiol")
OctC1 = ParseSASAInformation("/media/jje63/easystore/SingleNP_C1/Octanethiol")

TetSS = ParseSASAInformation("/media/jje63/easystore/SingleNP_SS/Tetracosanethiol")
TetQa = ParseSASAInformation("/media/jje63/easystore/SingleNP_Qa/Tetracosanethiol")
TetP5 = ParseSASAInformation("/media/jje63/easystore/SingleNP_P5/Tetracosanethiol")
TetC5 = ParseSASAInformation("/media/jje63/easystore/SingleNP_C5/Tetracosanethiol")
TetC1 = ParseSASAInformation("/media/jje63/easystore/SingleNP_C1/Tetracosanethiol")

DodC5 = ParseSASAInformation("/media/jje63/easystore/SingleNP_C5/Dodecanethiol")
HexC5 = ParseSASAInformation("/media/jje63/easystore/SingleNP_C5/Hexadecanethiol")
IcoC5 = ParseSASAInformation("/media/jje63/easystore/SingleNP_C5/Icosanethiol")
TetC5 = ParseSASAInformation("/media/jje63/easystore/SingleNP_C5/Tetracosanethiol")

DodP5 = ParseSASAInformation("/media/jje63/easystore/SingleNP_P5/Dodecanethiol")
HexP5 = ParseSASAInformation("/media/jje63/easystore/SingleNP_P5/Hexadecanethiol")
IcoP5 = ParseSASAInformation("/media/jje63/easystore/SingleNP_P5/Icosanethiol")
TetP5 = ParseSASAInformation("/media/jje63/easystore/SingleNP_P5/Tetracosanethiol")

xvalOctSS = AverageSASA(OctSS)
xvalOctQa = AverageSASA(OctQa)
xvalOctC1 = AverageSASA(OctC1)
xvalOctC5 = AverageSASA(OctC5)
xvalOctP5 = AverageSASA(OctP5)

stdOctSS = np.std(np.array(OctSS['NP1']))
stdOctQa = np.std(np.array(OctQa['NP1']))
stdOctC1 = np.std(np.array(OctC1['NP1']))
stdOctC5 = np.std(np.array(OctC5['NP1']))
stdOctP5 = np.std(np.array(OctP5['NP1']))

xvalTetSS = AverageSASA(TetSS)
xvalTetQa = AverageSASA(TetQa)
xvalTetC1 = AverageSASA(TetC1)
xvalTetC5 = AverageSASA(TetC5)
xvalTetP5 = AverageSASA(TetP5)

stdTetSS = np.std(np.array(TetSS['NP1']))
stdTetQa = np.std(np.array(TetQa['NP1']))
stdTetC1 = np.std(np.array(TetC1['NP1']))
stdTetC5 = np.std(np.array(TetC5['NP1']))
stdTetP5 = np.std(np.array(TetP5['NP1']))


xvalDodC5 = AverageSASA(DodC5)
xvalHexC5 = AverageSASA(HexC5)
xvalIcoC5 = AverageSASA(IcoC5)
xvalTetC5 = AverageSASA(TetC5)

xvalDodP5 = AverageSASA(DodP5)
xvalHexP5 = AverageSASA(HexP5)
xvalIcoP5 = AverageSASA(IcoP5)
xvalTetP5 = AverageSASA(TetP5)


AvgAll = [xvalOctC5,xvalDodC5,xvalHexC5,xvalIcoC5,xvalTetC5]
AvgAll2 = [xvalOctP5,xvalDodP5,xvalHexP5,xvalIcoP5,xvalTetP5]

figure, axs = plt.subplots(1, 1, figsize=(8,6))
#plt.plot([8,12,16,20,24],AvgAll,linestyle='solid',marker='^',markersize = 10,color="#439FEF",label="C5")
#plt.plot([8,12,16,20,24],AvgAll2,linestyle='solid',marker='^',markersize = 10,color="#BA6E6E",label="P5")

axs.errorbar(["C1","C5","SS","P5","Qa"],[xvalOctC1,xvalOctC5,xvalOctSS,xvalOctP5,xvalOctQa],yerr=[stdOctC1,stdOctC5,stdOctSS,stdOctP5,stdOctQa],linestyle='solid',marker='^',markersize = 10,color="red",label="Octanethiol")
axs.errorbar(["C1","C5","SS","P5","Qa"],[xvalTetC1,xvalTetC5,xvalTetSS,xvalTetP5,xvalTetQa],yerr=[stdTetC1,stdTetC5,stdTetSS,stdTetP5,stdTetQa],linestyle='solid',alpha=0.5,marker='^',markersize = 10,color="black",label="Tetracosanethiol")
axs.set_xlabel("Core Parameter", fontsize=25)
axs.set_ylabel("Water Accesible Surface Area ($nm^{2}$)", fontsize=18)
axs.tick_params(axis='y', labelsize=15)
axs.tick_params(axis='x', labelsize=15)
plt.legend(loc="upper left")

#plt.yticks(np.arange(0, 15, step=2))
plt.savefig("/media/jje63/easystore/Graphs/SASA_Coreposter.pdf",format='pdf',dpi=500, bbox_inches='tight')
"""

"""
Doddis = ParseDistanceInformation("/media/jje63/My Passport/SASARUN/SASAFull/distance.dat")
#print(Doddis[1])
Dod1 = ParseSASAInformation("/media/jje63/My Passport/SASARUN/SASAFull")
Order1 = ParseOrderParamTimeInformation("/media/jje63/My Passport/SASARUN/SASAFull/OrderOverTime",5)
figure , axs = plt.subplots(1, figsize=(10,8), sharex=True)
axs.plot(Dod1['NP1'][0][3:-3], np.array(medfilt(Dod1['NP1'][1], 21)[3:-3])/max(medfilt(Dod1['NP1'][1], 21)[3:-3]), linewidth = 4, label= "SASA")
axs.plot(Doddis[0][3:-3], np.array(medfilt(Doddis[1], 21)[3:-3])/max(medfilt(Doddis[1], 21)[3:-3]), color="orange", linewidth = 4, label= "Distance")
axs.plot(Order1[0][1:-2],np.array(medfilt(Order1[1],11)[1:-2])*(1/max(medfilt(Order1[1],11)[1:-2])),linestyle='solid',linewidth=4, color="black", label= "Order Parameter")
#axs.set_ylabel("SASA($nm^{2}$)")
axs.set_ylabel("Normalized Values") 
axs.set_xlabel("Time ($\mu s$)") 
axs.legend(loc="upper left",bbox_to_anchor=(1.0, 1.0),fontsize='large')
#axs[0].set_yticks(np.arange(25, 120 , step=15))
#axs[0].axvline(x = 137/100, color = 'black', linewidth= 0.5, label = 'axvline - full height')
#axs[1].axvline(x = 190/100, color = 'black', linewidth= 0.5, label = 'axvline - full height')
#axs[0].axvline(x = 190/100, color = 'black', linewidth= 0.5, label = 'axvline - full height')
plt.savefig("/media/jje63/easystore/Graphs/SASA_Distance_OrderParameter.pdf",format='pdf',dpi=500, bbox_inches='tight')
"""
"""
DimerNP = ParseSASAInformation("/media/jje63/My Passport/RossiGoldCoreTest/DimerNP")
Doddis = ParseDistanceInformation("/media/jje63/My Passport/RossiGoldCoreTest/DimerNP/distance.dat")
figure , axs = plt.subplots(1, figsize=(10,8), sharex=True)
axs.plot(DimerNP['NP1'][0][3:-3], np.array(medfilt(DimerNP['NP1'][1],5)[3:-3])/max(medfilt(DimerNP['NP1'][1], 5)[3:-3]), linewidth = 4, label= "SASA")
axs.plot(Doddis[0][3:-3], np.array(medfilt(Doddis[1], 21)[3:-3])/max(medfilt(Doddis[1], 21)[3:-3]), color="orange", linewidth = 4, label= "Distance")
"""
#plt.axvline(x = 114, color = 'b', linewidth=1, label = 'axvline - full height')
#plt.axvline(x = 798, color = 'b', linewidth=1, label = 'axvline - full height')
#axs[0].plot(Hex1['NP1'][0][1:],medfilt(Hex1['NP1'][1][1:], 15),color="red",linewidth=1)
# axs[0].set_ylabel("SASA")
# axs[0].plot(Hex1['NP2'][0],Hex1['NP2'][1])
# axs[1].plot(Agg1[0],Agg1[1])
# axs[1].set_ylabel("$F_{agg}$")
# axs[2].plot(LC1[0],medfilt(LC1[1],13))
#axs[2].set_ylabel("Lipid Coordination Number")
# axs[3].plot(WC1[0],medfilt(WC1[1],13))
#axs[3].set_ylabel("Water Coordination Number")
# print(list(Hex1.values())[0])

#plt.savefig("/media/jje63/easystore/Coverage/100Dodecanethiol/Aggregationpar.pdf",format='pdf',dpi=500, bbox_inches='tight')



## Probability Density ##
### Polar ###

P5Oct = ParseClusterInformation("/media/jje63/easystore/PolarNP/Octanethiol/ClusterAU10.dat")
P5Dod= ParseClusterInformation("/media/jje63/easystore/PolarNP/Dodecanthiol/ClusterAU10.dat")
P5Hex = ParseClusterInformation("/media/jje63/easystore/PolarNP/Hexadecanethiol/ClusterAU10.dat")
P5Ico = ParseClusterInformation("/media/jje63/easystore/PolarNP/Icosanethiol/ClusterAU10.dat")
P5Tet = ParseClusterInformation("/media/jje63/easystore/PolarNP/Tetracosanethiol/ClusterAU10.dat")


P5Oct2 = ParseClusterInformation("/media/jje63/easystore/PolarNP_2/Octanethiol/ClusterAU10.dat")
P5Dod2= ParseClusterInformation("/media/jje63/easystore/PolarNP_2/Dodecanthiol/ClusterAU10.dat")
P5Hex2 = ParseClusterInformation("/media/jje63/easystore/PolarNP_2/Hexadecanethiol/ClusterAU10.dat")
P5Ico2 = ParseClusterInformation("/media/jje63/easystore/PolarNP_2/Icosanethiol/ClusterAU10.dat")
P5Tet2 = ParseClusterInformation("/media/jje63/easystore/PolarNP_2/Tetracosanethiol/ClusterAU10.dat")

P5Oct3 = ParseClusterInformation("/media/jje63/easystore/PolarNP_3/Octanethiol/ClusterAU10.dat")
P5Dod3 = ParseClusterInformation("/media/jje63/easystore/PolarNP_3/Dodecanthiol/ClusterAU10.dat")
P5Hex3 = ParseClusterInformation("/media/jje63/easystore/PolarNP_3/Hexadecanethiol/ClusterAU10.dat")
P5Ico3 = ParseClusterInformation("/media/jje63/easystore/PolarNP_3/Icosanethiol/ClusterAU10.dat")
P5Tet3 = ParseClusterInformation("/media/jje63/easystore/PolarNP_3/Tetracosanethiol/ClusterAU10.dat")

P5Oct4 = ParseClusterInformation("/media/jje63/easystore/PolarNP_4/Octanethiol/ClusterAU10.dat")
P5Dod4 = ParseClusterInformation("/media/jje63/easystore/PolarNP_4/Dodecanthiol/ClusterAU10.dat")
P5Hex4 = ParseClusterInformation("/media/jje63/easystore/PolarNP_4/Hexadecanethiol/ClusterAU10.dat")
P5Ico4 = ParseClusterInformation("/media/jje63/easystore/PolarNP_4/Icosanethiol/ClusterAU10.dat")
P5Tet4 = ParseClusterInformation("/media/jje63/easystore/PolarNP_4/Tetracosanethiol/ClusterAU10.dat")

P5Oct5 = ParseClusterInformation("/media/jje63/easystore/PolarNP_5/Octanethiol/ClusterAU10.dat")
P5Dod5 = ParseClusterInformation("/media/jje63/easystore/PolarNP_5/Dodecanthiol/ClusterAU10.dat")
P5Hex5 = ParseClusterInformation("/media/jje63/easystore/PolarNP_5/Hexadecanethiol/ClusterAU10.dat")
P5Ico5 = ParseClusterInformation("/media/jje63/easystore/PolarNP_5/Icosanethiol/ClusterAU10.dat")
P5Tet5 = ParseClusterInformation("/media/jje63/easystore/PolarNP_5/Tetracosanethiol/ClusterAU10.dat")

P5Oct6 = ParseClusterInformation("/media/jje63/easystore/PolarNP_6/Octanethiol/ClusterAU10.dat")
P5Dod6 = ParseClusterInformation("/media/jje63/easystore/PolarNP_6/Dodecanthiol/ClusterAU10.dat")
P5Hex6 = ParseClusterInformation("/media/jje63/easystore/PolarNP_6/Hexadecanethiol/ClusterAU10.dat")
P5Ico6 = ParseClusterInformation("/media/jje63/easystore/PolarNP_6/Icosanethiol/ClusterAU10.dat")
P5Tet6 = ParseClusterInformation("/media/jje63/easystore/PolarNP_6/Tetracosanethiol/ClusterAU10.dat")

### Hydrophobic ###

C5Oct = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle/Octanethiol/ClusterAU10.dat")
C5Dod = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle/Dodecanthiol/ClusterAU10.dat")
C5Hex = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle/Hexadecanethiol/ClusterAU10.dat")
C5Ico = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle/Icosanethiol/ClusterAU10.dat")
C5Tet = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle/Tetracosanethiol/ClusterAU10.dat")

C5Oct2 = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle_2/Octanethiol/ClusterAU10.dat")
C5Dod2 = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle_2/Dodecanthiol/ClusterAU10.dat")
C5Hex2 = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle_2/Hexadecanethiol/ClusterAU10.dat")
C5Ico2 = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle_2/Icosanethiol/ClusterAU10.dat")
C5Tet2 = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle_2/Tetracosanethiol/ClusterAU10.dat")

C5Oct3 = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle_3/Octanethiol/ClusterAU10.dat")
C5Dod3 = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle_3/Dodecanthiol/ClusterAU10.dat")
C5Hex3 = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle_3/Hexadecanethiol/ClusterAU10.dat")
C5Ico3 = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle_3/Icosanethiol/ClusterAU10.dat")
C5Tet3 = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle_3/Tetracosanethiol/ClusterAU10.dat")

C5Oct4 = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle_4/Octanethiol/ClusterAU10.dat")
C5Dod4 = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle_4/Dodecanthiol/ClusterAU10.dat")
C5Hex4 = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle_4/Hexadecanethiol/ClusterAU10.dat")
C5Ico4 = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle_4/Icosanethiol/ClusterAU10.dat")
C5Tet4 = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle_4/Tetracosanethiol/ClusterAU10.dat")

C5Oct5 = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle_5/Octanethiol/ClusterAU10.dat")
C5Dod5 = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle_5/Dodecanthiol/ClusterAU10.dat")
C5Hex5 = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle_5/Hexadecanethiol/ClusterAU10.dat")
C5Ico5 = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle_5/Icosanethiol/ClusterAU10.dat")
C5Tet5 = ParseClusterInformation("/media/jje63/easystore/Common_Nanoparticle_5/Tetracosanethiol/ClusterAU10.dat")

### Soft Sphere ###
SSOct = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere/Octanethiol/ClusterAU10.dat")
SSDod = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere/Dodecanthiol/ClusterAU10.dat")
SSHex = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere/Hexadecanethiol/ClusterAU10.dat")
SSIco = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere/Icosanethiol/ClusterAU10.dat")
SSTet = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere/Tetracosanethiol/ClusterAU10.dat")

SSOct2 = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere_2/Octanethiol/ClusterAU10.dat")
SSDod2 = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere_2/Dodecanthiol/ClusterAU10.dat")
SSHex2 = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere_2/Hexadecanethiol/ClusterAU10.dat")
SSIco2 = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere_2/Icosanethiol/ClusterAU10.dat")
SSTet2 = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere_2/Tetracosanethiol/ClusterAU10.dat")

SSOct3 = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere_3/Octanethiol/ClusterAU10.dat")
SSDod3 = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere_3/Dodecanthiol/ClusterAU10.dat")
SSHex3 = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere_3/Hexadecanethiol/ClusterAU10.dat")
SSIco3 = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere_3/Icosanethiol/ClusterAU10.dat")
SSTet3 = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere_3/Tetracosanethiol/ClusterAU10.dat")

SSOct4 = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere_4/Octanethiol/ClusterAU10.dat")
SSDod4 = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere_4/Dodecanthiol/ClusterAU10.dat")
SSHex4 = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere_4/Hexadecanethiol/ClusterAU10.dat")
SSIco4 = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere_4/Icosanethiol/ClusterAU10.dat")
SSTet4 = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere_4/Tetracosanethiol/ClusterAU10.dat")

SSOct5 = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere_5/Octanethiol/ClusterAU10.dat")
SSDod5 = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere_5/Dodecanthiol/ClusterAU10.dat")
SSHex5 = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere_5/Hexadecanethiol/ClusterAU10.dat")
SSIco5 = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere_5/Icosanethiol/ClusterAU10.dat")
SSTet5 = ParseClusterInformation("/media/jje63/easystore/Soft_Sphere_5/Tetracosanethiol/ClusterAU10.dat")



### Large Hydrophobic ###

#LC5Oct = ParseClusterInformation("/media/jje63/easystore/Mega_NP_Sys_Hydrphobic/Octanethiol/ClusterAU10.dat")
#LC5Dod = ParseClusterInformation("/media/jje63/easystore/Mega_NP_Sys_Hydrphobic/Dodecanethiol/ClusterAU10.dat")
#LC5Hex = ParseClusterInformation("/media/jje63/easystore/Mega_NP_Sys_Hydrphobic/Hexadecanethiol/ClusterAU10.dat")
#LC5Ico = ParseClusterInformation("/media/jje63/easystore/Mega_NP_Sys_Hydrphobic/Icosanethiol/ClusterAU10.dat")
#LC5Tet = ParseClusterInformation("/media/jje63/easystore/Mega_NP_Sys_Hydrphobic/Tetracosanethiol/ClusterAU10.dat")

"""
QaOct = ParseClusterInformation("/media/jje63/easystore/Octanethiol/ClusterAU10.dat")
QaDod = ParseClusterInformation("/media/jje63/easystore/NP_Concentration/10np_membrane_3/ClusterAU10.dat")
QaHex = ParseClusterInformation("/media/jje63/easystore/Hexadecanethiol_1/ClusterAU10.dat")
QaIco = ParseClusterInformation("/media/jje63/easystore/Icosanethiol/ClusterAU10.dat")
QaTet = ParseClusterInformation("/media/jje63/easystore/Bridges2/jennis/Tetracosanethiol/tetracosanethiol_1/ClusterAU10.dat")

C1Oct = ParseClusterInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano/Octanethiol_P1/ClusterAU10.dat")
C1Dod = ParseClusterInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano/Dodecanethiol_C1/ClusterAU15.dat")
C1Hex = ParseClusterInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano/Hexadecanethiol_C1/ClusterAU10.dat")
C1Ico = ParseClusterInformation("/media/jje63/easystore/Bridges2/jennis/C1_Nano/Icosanethiol_C1/ClusterAU10.dat")
C1Tet = ParseClusterInformation("/media/jje63/easystore/Bridges2/jennis/Tetracosanethiol/tetracosanethiol_1C/ClusterAU10.dat")
"""

## Largest Cluster ##

"""C5OctAvg = [np.mean(C5Oct[1])/10,np.mean(C5Oct2[1])/10,np.mean(C5Oct3[1])/10,np.mean(C5Oct4[1])/10,np.mean(C5Oct5[1])/10]
C5DodAvg = [np.mean(C5Dod[1])/10,np.mean(C5Dod2[1])/10,np.mean(C5Dod3[1])/10,np.mean(C5Dod4[1])/10,np.mean(C5Dod5[1])/10]
C5HexAvg = [np.mean(C5Hex[1])/10,np.mean(C5Hex2[1])/10,np.mean(C5Hex3[1])/10,np.mean(C5Hex4[1])/10,np.mean(C5Hex5[1])/10]
C5IcoAvg = [np.mean(C5Ico[1])/10,np.mean(C5Ico2[1])/10,np.mean(C5Ico3[1])/10,np.mean(C5Ico4[1])/10,np.mean(C5Ico5[1])/10]
C5TetAvg = [np.mean(C5Tet[1])/10,np.mean(C5Tet2[1])/10,np.mean(C5Tet3[1])/10,np.mean(C5Tet4[1])/10,np.mean(C5Tet5[1])/10]

P5OctAvg = [np.mean(P5Oct[1])/10,np.mean(P5Oct2[1])/10,np.mean(P5Oct3[1])/10,np.mean(P5Oct4[1])/10,np.mean(P5Oct5[1])/10,np.mean(P5Oct6[1])/10]
P5DodAvg = [np.mean(P5Dod[1])/10,np.mean(P5Dod2[1])/10,np.mean(P5Dod3[1])/10,np.mean(P5Dod4[1])/10,np.mean(P5Dod5[1])/10,np.mean(P5Dod6[1])/10]
P5HexAvg = [np.mean(P5Hex[1])/10,np.mean(P5Hex2[1])/10,np.mean(P5Hex3[1])/10,np.mean(P5Hex4[1])/10,np.mean(P5Hex5[1])/10,np.mean(P5Hex6[1])/10]
P5IcoAvg = [np.mean(P5Ico[1])/10,np.mean(P5Ico2[1])/10,np.mean(P5Ico3[1])/10,np.mean(P5Ico4[1])/10,np.mean(P5Ico5[1])/10,np.mean(P5Ico6[1])/10]
P5TetAvg = [np.mean(P5Tet[1])/10,np.mean(P5Tet2[1])/10,np.mean(P5Tet3[1])/10,np.mean(P5Tet4[1])/10,np.mean(P5Tet5[1])/10,np.mean(P5Tet6[1])/10]

SSOctAvg = [np.mean(SSOct[1])/10,np.mean(SSOct2[1])/10,np.mean(SSOct3[1])/10,np.mean(SSOct4[1])/10,np.mean(SSOct5[1])/10]
SSDodAvg = [np.mean(SSDod[1])/10,np.mean(SSDod2[1])/10,np.mean(SSDod3[1])/10,np.mean(SSDod4[1])/10,np.mean(SSDod5[1])/10]
SSHexAvg = [np.mean(SSHex[1])/10,np.mean(SSHex2[1])/10,np.mean(SSHex3[1])/10,np.mean(SSHex4[1])/10,np.mean(SSHex5[1])/10]
SSIcoAvg = [np.mean(SSIco[1])/10,np.mean(SSIco2[1])/10,np.mean(SSIco3[1])/10,np.mean(SSIco4[1])/10,np.mean(SSIco5[1])/10]
SSTetAvg = [np.mean(SSTet[1])/10,np.mean(SSTet2[1])/10,np.mean(SSTet3[1])/10,np.mean(SSTet4[1])/10,np.mean(SSTet5[1])/10]
"""

## Monomer Fraction ##

C5OctAvg  = [np.mean(C5Oct[2])/10,np.mean(C5Oct2[2])/10,np.mean(C5Oct3[2])/10,np.mean(C5Oct4[2])/10,np.mean(C5Oct5[2])/10]
C5DodAvg = [np.mean(C5Dod[2])/10,np.mean(C5Dod2[2])/10,np.mean(C5Dod3[2])/10,np.mean(C5Dod4[2])/10,np.mean(C5Dod5[2])/10]
C5HexAvg = [np.mean(C5Hex[2])/10,np.mean(C5Hex2[2])/10,np.mean(C5Hex3[2])/10,np.mean(C5Hex4[2])/10,np.mean(C5Hex5[2])/10]
C5IcoAvg = [np.mean(C5Ico[2])/10,np.mean(C5Ico2[2])/10,np.mean(C5Ico3[2])/10,np.mean(C5Ico4[2])/10,np.mean(C5Ico5[2])/10]
C5TetAvg = [np.mean(C5Tet[2])/10,np.mean(C5Tet2[2])/10,np.mean(C5Tet3[2])/10,np.mean(C5Tet4[2])/10,np.mean(C5Tet5[2])/10]


P5OctAvg = [np.mean(P5Oct[2])/10,np.mean(P5Oct2[2])/10,np.mean(P5Oct3[2])/10,np.mean(P5Oct4[2])/10,np.mean(P5Oct5[2])/10,np.mean(P5Oct6[2])/10]
P5DodAvg = [np.mean(P5Dod[2])/10,np.mean(P5Dod2[2])/10,np.mean(P5Dod3[2])/10,np.mean(P5Dod4[2])/10,np.mean(P5Dod5[2])/10,np.mean(P5Dod6[2])/10]
P5HexAvg = [np.mean(P5Hex[2])/10,np.mean(P5Hex2[2])/10,np.mean(P5Hex3[2])/10,np.mean(P5Hex4[2])/10,np.mean(P5Hex5[2])/10,np.mean(P5Hex6[2])/10]
P5IcoAvg = [np.mean(P5Ico[2])/10,np.mean(P5Ico2[2])/10,np.mean(P5Ico3[2])/10,np.mean(P5Ico4[2])/10,np.mean(P5Ico5[2])/10,np.mean(P5Ico6[2])/10]
P5TetAvg = [np.mean(P5Tet[2])/10,np.mean(P5Tet2[2])/10,np.mean(P5Tet3[2])/10,np.mean(P5Tet4[2])/10,np.mean(P5Tet5[2])/10,np.mean(P5Tet6[2])/10]

"""SSOctAvg = [np.mean(SSOct[2])/10,np.mean(SSOct2[2])/10,np.mean(SSOct3[2])/10,np.mean(SSOct4[2])/10,np.mean(SSOct5[2])/10]
SSDodAvg = [np.mean(SSDod[2])/10,np.mean(SSDod2[2])/10,np.mean(SSDod3[2])/10,np.mean(SSDod4[2])/10,np.mean(SSDod5[2])/10]
SSHexAvg = [np.mean(SSHex[2])/10,np.mean(SSHex2[2])/10,np.mean(SSHex3[2])/10,np.mean(SSHex4[2])/10,np.mean(SSHex5[2])/10]
SSIcoAvg = [np.mean(SSIco[2])/10,np.mean(SSIco2[2])/10,np.mean(SSIco3[2])/10,np.mean(SSIco4[2])/10,np.mean(SSIco5[2])/10]
SSTetAvg = [np.mean(SSTet[2])/10,np.mean(SSTet2[2])/10,np.mean(SSTet3[2])/10,np.mean(SSTet4[2])/10,np.mean(SSTet5[2])/10]
"""
"""
## Average Aggregate Size ##
C5OctAvg = [np.mean(C5Oct[3]),np.mean(C5Oct2[3]),np.mean(C5Oct3[3]),np.mean(C5Oct4[3]),np.mean(C5Oct5[3])]
C5DodAvg = [np.mean(C5Dod[3]),np.mean(C5Dod2[3]),np.mean(C5Dod3[3]),np.mean(C5Dod4[3]),np.mean(C5Dod5[3])]
C5HexAvg = [np.mean(C5Hex[3]),np.mean(C5Hex2[3]),np.mean(C5Hex3[3]),np.mean(C5Hex4[3]),np.mean(C5Hex5[3])]
C5IcoAvg = [np.mean(C5Ico[3]),np.mean(C5Ico2[3]),np.mean(C5Ico3[3]),np.mean(C5Ico4[3]),np.mean(C5Ico5[3])]
C5TetAvg = [np.mean(C5Tet[3]),np.mean(C5Tet2[3]),np.mean(C5Tet3[3]),np.mean(C5Tet4[3]),np.mean(C5Tet5[3])]

P5OctAvg = [np.mean(P5Oct[3]),np.mean(P5Oct2[3]),np.mean(P5Oct3[3]),np.mean(P5Oct4[3]),np.mean(P5Oct5[3]),np.mean(P5Oct6[3])]
P5DodAvg = [np.mean(P5Dod[3]),np.mean(P5Dod2[3]),np.mean(P5Dod3[3]),np.mean(P5Dod4[3]),np.mean(P5Dod5[3]),np.mean(P5Dod6[3])]
P5HexAvg = [np.mean(P5Hex[3]),np.mean(P5Hex2[3]),np.mean(P5Hex3[3]),np.mean(P5Hex4[3]),np.mean(P5Hex5[3]),np.mean(P5Hex6[3])]
P5IcoAvg = [np.mean(P5Ico[3]),np.mean(P5Ico2[3]),np.mean(P5Ico3[3]),np.mean(P5Ico4[3]),np.mean(P5Ico5[3]),np.mean(P5Ico6[3])]
P5TetAvg = [np.mean(P5Tet[3]),np.mean(P5Tet2[3]),np.mean(P5Tet3[3]),np.mean(P5Tet4[3]),np.mean(P5Tet5[3]),np.mean(P5Tet6[3])]

SSOctAvg = [np.mean(SSOct[3]),np.mean(SSOct2[3]),np.mean(SSOct3[3]),np.mean(SSOct4[3]),np.mean(SSOct5[3])]
SSDodAvg = [np.mean(SSDod[3]),np.mean(SSDod2[3]),np.mean(SSDod3[3]),np.mean(SSDod4[3]),np.mean(SSDod5[3])]
SSHexAvg = [np.mean(SSHex[3]),np.mean(SSHex2[3]),np.mean(SSHex3[3]),np.mean(SSHex4[3]),np.mean(SSHex5[3])]
SSIcoAvg = [np.mean(SSIco[3]),np.mean(SSIco2[3]),np.mean(SSIco3[3]),np.mean(SSIco4[3]),np.mean(SSIco5[3])]
SSTetAvg = [np.mean(SSTet[3]),np.mean(SSTet2[3]),np.mean(SSTet3[3]),np.mean(SSTet4[3]),np.mean(SSTet5[3])]
"""


### Flat Average ###


"""binn = np.arange(1,12,1)

def Concatenate_histogram_lig(all_rep, bins):
    n_holder = []
    data = np.concatenate(all_rep)
    n, bins, patches = plt.hist(data, bins, density=True, histtype='step', cumulative=-1)
    for rep in all_rep:
        n2, bins2, patches = plt.hist(rep, bins, density=True, histtype='step', cumulative=-1)
        n_holder.append(n2)
    std = np.std(n_holder, axis=0)/np.sqrt(5)
    return [n, std]

#def Concatenate_histogram_rep(all_rep, bins):
    

def full_loop_hist(full_reps, bins):
    Histo_data = []
    std = []
    for data in full_reps:
        data, stand = Concatenate_histogram_lig(data, bins)
        Histo_data.append(data)
        std.append(stand)
    Histo_data = np.array(Histo_data)
    std = np.array(std)
    return [Histo_data, std]"""





# P5OctAll = [P5Oct[4],P5Oct2[4],P5Oct3[4],P5Oct4[4],P5Oct5[4]]
# P5DodAll = [P5Dod[4],P5Dod2[4],P5Dod3[4],P5Dod4[4],P5Dod5[4]]
# P5HexAll = [P5Hex[4],P5Hex2[4],P5Hex3[4],P5Hex4[4],P5Hex5[4]]
# P5IcoAll = [P5Ico[4],P5Ico2[4],P5Ico3[4],P5Ico4[4],P5Ico5[4]]
# P5TetAll = [P5Tet[4],P5Tet2[4],P5Tet3[4],P5Tet4[4],P5Tet5[4]]
# 
# SSOctAll = [SSOct[4],SSOct2[4],SSOct3[4],SSOct4[4],SSOct5[4]]
# SSDodAll = [SSDod[4],SSDod2[4],SSDod3[4],SSDod4[4],SSDod5[4]]
# SSHexAll = [SSHex[4],SSHex2[4],SSHex3[4],SSHex4[4],SSHex5[4]]
# SSIcoAll = [SSIco[4],SSIco2[4],SSIco3[4],SSIco4[4],SSIco5[4]]
# SSTetAll = [SSTet[4],SSTet2[4],SSTet3[4],SSTet4[4],SSTet5[4]]
# 
#C5OctAll = [C5Oct[2],C5Oct2[2],C5Oct3[2],C5Oct4[2],C5Oct5[2]]
#print(C5OctAll)
#C5DodAll = [C5Dod[4],C5Dod2[4],C5Dod3[4],C5Dod4[4],C5Dod5[4]]
#C5HexAll = [C5Hex[4],C5Hex2[4],C5Hex3[4],C5Hex4[4],C5Hex5[4]]
#C5IcoAll = [C5Ico[4],C5Ico2[4],C5Ico3[4],C5Ico4[4],C5Ico5[4]]
#C5TetAll = [C5Tet[4],C5Tet2[4],C5Tet3[4],C5Tet4[4],C5Tet5[4]]
# 
# All_list_P5 = [P5OctAll, P5DodAll, P5HexAll, P5IcoAll, P5TetAll]
# All_list_SS = [SSOctAll, SSDodAll, SSHexAll, SSIcoAll, SSTetAll]
# All_list_C5 = [C5OctAll, C5DodAll, C5HexAll, C5IcoAll, C5TetAll]
# 
# 
# Hist, std = full_loop_hist(All_list_P5, binn)
# 
# figure , axs = plt.subplots(1, figsize=(8,6), sharex=True)
# axs.plot(binn[:-1], Hist[0], label= "Octanethiol",linewidth=3,color="#ff595e")
# axs.fill_between(binn[:-1],Hist[0]-std[0],Hist[0]+std[0],color="#ff595e",alpha=0.2)
# axs.plot(binn[:-1], Hist[1], label= "Dodecanethiol",linewidth=3,color="#ffca3a")
# axs.fill_between(binn[:-1],Hist[1]-std[1],Hist[1]+std[1],color="#ffca3a",alpha=0.2)
# axs.plot(binn[:-1], Hist[2], label= "Hexadecanethiol",linewidth=3,color="#8ac926")
# axs.fill_between(binn[:-1],Hist[2]-std[2],Hist[2]+std[2],color="#8ac926",alpha=0.2)
# axs.plot(binn[:-1], Hist[3], label= "Icosanethiol",linewidth=3,color="#1982c4")
# axs.fill_between(binn[:-1],Hist[3]-std[3],Hist[3]+std[3],color="#1982c4",alpha=0.2)
# axs.plot(binn[:-1], Hist[4], label= "Tetracosanethiol",linewidth=3,color="#6a4c93")
# axs.fill_between(binn[:-1],Hist[4]-std[4],Hist[4]+std[4],color="#6a4c93",alpha=0.2)
# 
# #axs.set_ylabel(r'$P(n_{agg})$',size=25)
# #axs.set_ylabel("Inverse " r'$CDF(n_{agg})$',size=15)
# axs.set_ylabel(r'$CDF(n_{agg})$',size=15)
# axs.set_xlabel("Aggregate Size",size=15)
# # #axs.tick_params(axis='y', labelsize=15)
# # #axs.tick_params(axis='x', labelsize=15)
# axs.legend(loc="upper right")
# axs.set_xticks(np.arange(1, 11, step=1))
# # axs.set_yticks(np.arange(0, 1.1, step=0.2))
# plt.savefig("/media/jje63/easystore/Graphs/CDF_GNP_LL_polar.pdf",format='pdf',dpi=500, bbox_inches='tight')


"""P5OctAll = P5Oct[4]+P5Oct2[4]+P5Oct3[4]+P5Oct4[4]+P5Oct5[4]
P5DodAll = P5Dod[4]+P5Dod2[4]+P5Dod3[4]+P5Dod4[4]+P5Dod5[4]
P5HexAll = P5Hex[4]+P5Hex2[4]+P5Hex3[4]+P5Hex4[4]+P5Hex5[4]
P5IcoAll = P5Ico[4]+P5Ico2[4]+P5Ico3[4]+P5Ico4[4]+P5Ico5[4]
P5TetAll = P5Tet[4]+P5Tet2[4]+P5Tet3[4]+P5Tet4[4]+P5Tet5[4]

P5HexAll = P5Hex[4] +P5Hex2[4]+P5Hex3[4]+P5Hex4[4]+P5Hex5[4]
P5IcoAll = P5Ico[4] +P5Ico2[4]+P5Ico3[4]+P5Ico4[4]+P5Ico5[4]
P5TetAll = P5Tet[4] +P5Tet2[4]+P5Tet3[4]+P5Tet4[4]+P5Tet5[4]

P5 = P5OctAll+P5DodAll+P5HexAll+P5IcoAll+P5TetAll
P5R1 = P5Oct[4]+P5Dod[4]+P5Hex[4]+P5Ico[4]+P5Tet[4]
P5R2 = P5Oct2[4]+P5Dod2[4]+P5Hex2[4]+P5Ico2[4]+P5Tet2[4]
P5R3 = P5Oct3[4]+P5Dod3[4]+P5Hex3[4]+P5Ico3[4]+P5Tet3[4]
P5R4 = P5Oct4[4]+P5Dod4[4]+P5Hex4[4]+P5Ico4[4]+P5Tet4[4]
P5R5 = P5Oct5[4]+P5Dod5[4]+P5Hex5[4]+P5Ico5[4]+P5Tet5[4]

P5Rep1 = np.histogram(P5R1,bins=binn,density=True)
P5Rep2 = np.histogram(P5R2,bins=binn,density=True)
P5Rep3 = np.histogram(P5R3,bins=binn,density=True)
P5Rep4 = np.histogram(P5R4,bins=binn,density=True)
P5Rep5 = np.histogram(P5R5,bins=binn,density=True)

#print(P5Rep1[0])

PRst1 = np.std([P5Rep1[0][0],P5Rep2[0][0],P5Rep3[0][0],P5Rep4[0][0],P5Rep5[0][0]])/np.sqrt(5)
PRst2 = np.std([P5Rep1[0][1],P5Rep2[0][1],P5Rep3[0][1],P5Rep4[0][1],P5Rep5[0][1]])/np.sqrt(5)
PRst3 = np.std([P5Rep1[0][2],P5Rep2[0][2],P5Rep3[0][2],P5Rep4[0][2],P5Rep5[0][2]])/np.sqrt(5)
PRst4 = np.std([P5Rep1[0][3],P5Rep2[0][3],P5Rep3[0][3],P5Rep4[0][3],P5Rep5[0][3]])/np.sqrt(5)
PRst5 = np.std([P5Rep1[0][4],P5Rep2[0][4],P5Rep3[0][4],P5Rep4[0][4],P5Rep5[0][4]])/np.sqrt(5)
PRst6 = np.std([P5Rep1[0][5],P5Rep2[0][5],P5Rep3[0][5],P5Rep4[0][5],P5Rep5[0][5]])/np.sqrt(5)
PRst7 = np.std([P5Rep1[0][6],P5Rep2[0][6],P5Rep3[0][6],P5Rep4[0][6],P5Rep5[0][6]])/np.sqrt(5)
PRst8 = np.std([P5Rep1[0][7],P5Rep2[0][7],P5Rep3[0][7],P5Rep4[0][7],P5Rep5[0][7]])/np.sqrt(5) 
PRst9 = np.std([P5Rep1[0][8],P5Rep2[0][8],P5Rep3[0][8],P5Rep4[0][8],P5Rep5[0][8]])/np.sqrt(5)
PRst10 = np.std([P5Rep1[0][9],P5Rep2[0][9],P5Rep3[0][9],P5Rep4[0][9],P5Rep5[0][9]])/np.sqrt(5)

P5error = [PRst1,PRst2,PRst3,PRst4,PRst5,PRst6,PRst7,PRst8,PRst9,PRst10]


SSOctAll = SSOct[4] +SSOct2[4]+SSOct3[4]+SSOct4[4]+SSOct5[4]
SSDodAll = SSDod[4] +SSDod2[4]+SSDod3[4]+SSDod4[4]+SSDod5[4]
SSHexAll = SSHex[4] +SSHex2[4]+SSHex3[4]+SSHex4[4]+SSHex5[4]
SSIcoAll = SSIco[4] +SSIco2[4]+SSIco3[4]+SSIco4[4]+SSIco5[4]
SSTetAll = SSTet[4] +SSTet2[4]+SSTet3[4]+SSTet4[4]+SSTet5[4]

SS = SSOctAll+SSDodAll+SSHexAll+SSIcoAll+SSTetAll
SSR1 = SSOct[4]+SSDod[4]+SSHex[4]+SSIco[4]+SSTet[4]
SSR2 = SSOct2[4]+SSDod2[4]+SSHex2[4]+SSIco2[4]+SSTet2[4]
SSR3 = SSOct3[4]+SSDod3[4]+SSHex3[4]+SSIco3[4]+SSTet3[4]
SSR4 = SSOct4[4]+SSDod4[4]+SSHex4[4]+SSIco4[4]+SSTet4[4]
SSR5 = SSOct5[4]+SSDod5[4]+SSHex5[4]+SSIco5[4]+SSTet5[4]

SSRep1 = np.histogram(SSR1,bins=binn,density=True)
SSRep2 = np.histogram(SSR2,bins=binn,density=True)
SSRep3 = np.histogram(SSR3,bins=binn,density=True)
SSRep4 = np.histogram(SSR4,bins=binn,density=True)
SSRep5 = np.histogram(SSR5,bins=binn,density=True)

SSst1 = np.std([SSRep1[0][0],SSRep2[0][0],SSRep3[0][0],SSRep4[0][0],SSRep5[0][0]])/np.sqrt(5)
SSst2 = np.std([SSRep1[0][1],SSRep2[0][1],SSRep3[0][1],SSRep4[0][1],SSRep5[0][1]])/np.sqrt(5)
SSst3 = np.std([SSRep1[0][2],SSRep2[0][2],SSRep3[0][2],SSRep4[0][2],SSRep5[0][2]])/np.sqrt(5)
SSst4 = np.std([SSRep1[0][3],SSRep2[0][3],SSRep3[0][3],SSRep4[0][3],SSRep5[0][3]])/np.sqrt(5)
SSst5 = np.std([SSRep1[0][4],SSRep2[0][4],SSRep3[0][4],SSRep4[0][4],SSRep5[0][4]])/np.sqrt(5)
SSst6 = np.std([SSRep1[0][5],SSRep2[0][5],SSRep3[0][5],SSRep4[0][5],SSRep5[0][5]])/np.sqrt(5)
SSst7 = np.std([SSRep1[0][6],SSRep2[0][6],SSRep3[0][6],SSRep4[0][6],SSRep5[0][6]])/np.sqrt(5)
SSst8 = np.std([SSRep1[0][7],SSRep2[0][7],SSRep3[0][7],SSRep4[0][7],SSRep5[0][7]])/np.sqrt(5) 
SSst9 = np.std([SSRep1[0][8],SSRep2[0][8],SSRep3[0][8],SSRep4[0][8],SSRep5[0][8]])/np.sqrt(5)
SSst10 = np.std([SSRep1[0][9],SSRep2[0][9],SSRep3[0][9],SSRep4[0][9],SSRep5[0][9]])/np.sqrt(5)

SSerror = [SSst1,SSst2,SSst3,SSst4,SSst5,SSst6,SSst7,SSst8,SSst9,SSst10]


LC5OctAll = LC5Oct[4] 
LC5DodAll = LC5Dod[4] 
LC5HexAll = LC5Hex[4] 
LC5IcoAll = LC5Ico[4] 
LC5TetAll = LC5Tet[4]
LC5 = LC5OctAll+LC5DodAll+LC5HexAll+LC5IcoAll+LC5TetAll

C5OctAll = np.concatenate([C5Oct[4],C5Oct2[4],C5Oct3[4],C5Oct4[4],C5Oct5[4]])
C5DodAll = np.concatenate([C5Dod[4],C5Dod2[4],C5Dod3[4],C5Dod4[4],C5Dod5[4]])
C5HexAll = np.concatenate([C5Hex[4],C5Hex2[4],C5Hex3[4],C5Hex4[4],C5Hex5[4]])
C5IcoAll = np.concatenate([C5Ico[4],C5Ico2[4],C5Ico3[4],C5Ico4[4],C5Ico5[4]])
C5TetAll = np.concatenate([C5Tet[4],C5Tet2[4],C5Tet3[4],C5Tet4[4],C5Tet5[4]])
C5 = np.concatenate([C5OctAll,C5DodAll,C5HexAll,C5IcoAll,C5TetAll])
#data = [P5OctAll,P5DodAll,P5HexAll,P5IcoAll,LC5TetAll]

C5R1 = C5Oct[4]+C5Dod[4]+C5Hex[4]+P5Ico[4]+P5Tet[4]
C5R2 = C5Oct2[4]+C5Dod2[4]+C5Hex2[4]+C5Ico2[4]+C5Tet2[4]
C5R3 = C5Oct3[4]+C5Dod3[4]+C5Hex3[4]+C5Ico3[4]+C5Tet3[4]
C5R4 = C5Oct4[4]+C5Dod4[4]+C5Hex4[4]+C5Ico4[4]+C5Tet4[4]
C5R5 = C5Oct5[4]+C5Dod5[4]+C5Hex5[4]+C5Ico5[4]+C5Tet5[4]

C5Rep1 = np.histogram(C5R1,bins=binn,density=True)
C5Rep2 = np.histogram(C5R2,bins=binn,density=True)
C5Rep3 = np.histogram(C5R3,bins=binn,density=True)
C5Rep4 = np.histogram(C5R4,bins=binn,density=True)
C5Rep5 = np.histogram(C5R5,bins=binn,density=True)

CRst1 = np.std([C5Rep1[0][0],C5Rep2[0][0],C5Rep3[0][0],C5Rep4[0][0],C5Rep5[0][0]])/np.sqrt(5)
CRst2 = np.std([C5Rep1[0][1],C5Rep2[0][1],C5Rep3[0][1],C5Rep4[0][1],C5Rep5[0][1]])/np.sqrt(5)
CRst3 = np.std([C5Rep1[0][2],C5Rep2[0][2],C5Rep3[0][2],C5Rep4[0][2],C5Rep5[0][2]])/np.sqrt(5)
CRst4 = np.std([C5Rep1[0][3],C5Rep2[0][3],C5Rep3[0][3],C5Rep4[0][3],C5Rep5[0][3]])/np.sqrt(5)
CRst5 = np.std([C5Rep1[0][4],C5Rep2[0][4],C5Rep3[0][4],C5Rep4[0][4],C5Rep5[0][4]])/np.sqrt(5)
CRst6 = np.std([C5Rep1[0][5],C5Rep2[0][5],C5Rep3[0][5],C5Rep4[0][5],C5Rep5[0][5]])/np.sqrt(5)
CRst7 = np.std([C5Rep1[0][6],C5Rep2[0][6],C5Rep3[0][6],C5Rep4[0][6],C5Rep5[0][6]])/np.sqrt(5)
CRst8 = np.std([C5Rep1[0][7],C5Rep2[0][7],C5Rep3[0][7],C5Rep4[0][7],C5Rep5[0][7]])/np.sqrt(5) 
CRst9 = np.std([C5Rep1[0][8],C5Rep2[0][8],C5Rep3[0][8],C5Rep4[0][8],C5Rep5[0][8]])/np.sqrt(5)
CRst10 = np.std([C5Rep1[0][9],C5Rep2[0][9],C5Rep3[0][9],C5Rep4[0][9],C5Rep5[0][9]])/np.sqrt(5)


C5error = [CRst1,CRst2,CRst3,CRst4,CRst5,CRst6,CRst7,CRst8,CRst9,CRst10]

#Oct_his = np.histogram(P5OctAll,bins=binn,density=True)
#Dod_his = np.histogram(P5DodAll,bins=binn,density=True)
#Hex_his = np.histogram(P5HexAll,bins=binn,density=True)
#Ico_his = np.histogram(P5IcoAll,bins=binn,density=True)
#Tet_his = np.histogram(P5TetAll,bins=binn,density=True)


Oct_his = np.histogram(C5OctAll,bins=binn,density=True)
Dod_his = np.histogram(C5DodAll,bins=binn,density=True)
Hex_his = np.histogram(C5HexAll,bins=binn,density=True)
Ico_his = np.histogram(C5IcoAll,bins=binn,density=True)
Tet_his = np.histogram(C5TetAll,bins=binn,density=True)

### Ligand Length STD ###
R1_Oct_P5 = np.histogram(C5Oct[4],bins=binn,density=True)
R2_Oct_P5 = np.histogram(C5Oct2[4],bins=binn,density=True)
R3_Oct_P5 = np.histogram(C5Oct3[4],bins=binn,density=True)
R4_Oct_P5 = np.histogram(C5Oct4[4],bins=binn,density=True)
R5_Oct_P5 = np.histogram(C5Oct5[4],bins=binn,density=True)



R1_Dod_P5 = np.histogram(P5Dod[4],bins=binn,density=True)
R2_Dod_P5 = np.histogram(P5Dod2[4],bins=binn,density=True)
R3_Dod_P5 = np.histogram(P5Dod3[4],bins=binn,density=True)
R4_Dod_P5 = np.histogram(P5Dod4[4],bins=binn,density=True)
R5_Dod_P5 = np.histogram(P5Dod5[4],bins=binn,density=True)


R1_Hex_P5 = np.histogram(P5Hex[4],bins=binn,density=True)
R2_Hex_P5 = np.histogram(P5Hex2[4],bins=binn,density=True)
R3_Hex_P5 = np.histogram(P5Hex3[4],bins=binn,density=True)
R4_Hex_P5 = np.histogram(P5Hex4[4],bins=binn,density=True)
R5_Hex_P5 = np.histogram(P5Hex5[4],bins=binn,density=True)



R1_Ico_P5 = np.histogram(P5Ico[4],bins=binn,density=True)
R2_Ico_P5 = np.histogram(P5Ico2[4],bins=binn,density=True)
R3_Ico_P5 = np.histogram(P5Ico3[4],bins=binn,density=True)
R4_Ico_P5 = np.histogram(P5Ico4[4],bins=binn,density=True)
R5_Ico_P5 = np.histogram(P5Ico5[4],bins=binn,density=True)


R1_Tet_P5 = np.histogram(P5Tet[4],bins=binn,density=True)
R2_Tet_P5 = np.histogram(P5Tet2[4],bins=binn,density=True)
R3_Tet_P5 = np.histogram(P5Tet3[4],bins=binn,density=True)
R4_Tet_P5 = np.histogram(P5Tet4[4],bins=binn,density=True)
R5_Tet_P5 = np.histogram(P5Tet5[4],bins=binn,density=True)


Polar = np.histogram(P5,bins=binn,density=True)
Hydro = np.histogram(C5,bins=binn,density=True)
softsphere = np.histogram(SS,bins=binn,density=True)

lHydro = np.histogram(LC5,bins=binn,density=True)

### Cumlulative density ###

#print(Oct_his[0])
#print(sum(Oct_his[0]))

CumlpolPolar = Polar[0] /sum(Polar[0])
CumlpolHydro = Hydro[0] /sum(Hydro[0])
CumlpolSS = softsphere[0] /sum(softsphere[0])
Cumlpollhyd = softsphere[0] /sum(lHydro[0])


cdfPol = np.flipud(np.flipud(CumlpolPolar).cumsum())
cdfHyd = np.flipud(np.flipud(CumlpolHydro).cumsum())
cdfSS = np.flipud(np.flipud(CumlpolSS).cumsum())

cdflhyd = np.flipud(np.flipud(Cumlpollhyd).cumsum())


plt.show() 
figure , axs = plt.subplots(1, figsize=(8,6), sharex=True)

#axs.plot(binn[:-1], cdfOct, label= "Octanethiol",linewidth=3,color="#ff595e")

#axs.fill_between(binn[:-1],cdfOct-Oct_his_std,cdfOct+Oct_his_std,color="#ff595e",alpha=0.2)
#axs.plot(binn[:-1], cdfDod, label= "Dodecanethiol",linewidth=3,color="#ffca3a")
#axs.fill_between(binn[:-1],cdfDod-Dod_his_std,cdfDod+Dod_his_std,color="#ffca3a",alpha=0.2)
#axs.plot(binn[:-1], cdfHex, label= "Hexadecanethiol",linewidth=3,color="#8ac926")
#axs.fill_between(binn[:-1],cdfHex-Hex_his_std,cdfHex+Hex_his_std,color="#8ac926",alpha=0.2)
#axs.plot(binn[:-1], cdfIco, label= "Icosanethiol",linewidth=3,color="#1982c4")
#axs.fill_between(binn[:-1],cdfIco-Ico_his_std,cdfIco+Ico_his_std,color="#1982c4",alpha=0.2)
#axs.plot(binn[:-1], cdfTet, label= "Tetracosanethiol",linewidth=3,color="#6a4c93")
#axs.fill_between(binn[:-1],cdfTet-Tet_his_std,cdfTet+Tet_his_std,color="#6a4c93",alpha=0.2)

axs.plot(binn[:-1], cdfPol, label= "Polar",linewidth=3,color="#fc8900")
axs.fill_between(binn[:-1],cdfPol-P5error,cdfPol+P5error,color="#fc8900",alpha=0.2)
axs.plot(binn[:-1], cdfHyd, label= "Hydrophobic",linewidth=3,color="#003dfc")
axs.fill_between(binn[:-1],cdfHyd-C5error,cdfHyd+C5error,color="#003dfc",alpha=0.2)
axs.plot(binn[:-1], cdfSS, label= "Soft Sphere",linewidth=3,color="grey")
axs.fill_between(binn[:-1],cdfSS-SSerror,cdfSS+SSerror,color="grey",alpha=0.2)

#axs.plot(binn[:-1], cdfDod, label= "10np",linewidth=3,color="#003dfc")
#axs.plot(binn[:-1], cdflhyd, label= "20np",linewidth=3,color="#a9d6e5")

#axs.plot(binn[:-1], Oct_his[0], label= "Octanethiol",linewidth=3,color="#ff595e")
#axs.plot(binn[:-1], Dod_his[0], label= "Dodecanethiol",linewidth=3,color="#ffca3a")
#axs.plot(binn[:-1], Hex_his[0], label= "Hexadecanethiol",linewidth=3,color="#8ac926")
#axs.plot(binn[:-1], Ico_his[0], label= "Icosanethiol",linewidth=3,color="#1982c4")
#axs.plot(binn[:-1], Tet_his[0], label= "Tetracosanethiol",linewidth=3,color="#6a4c93")

#axs.errorbar(Polar[1][:-1],Polar[0], label="Polar",linewidth=3,color="#fc8900",capsize=8)
#axs.errorbar(Hydro[1][:-1],Hydro[0],alpha=0.5, label="Hydrophobic",linewidth=3,color="#003dfc",capsize=8)
#axs.errorbar(softsphere[1][:-1],softsphere[0], label="Soft Sphere",linewidth=3,color="grey",capsize=8)
#axs.plot(lHydro[1][:-1],lHydro[0], label="20np",linewidth=3,color="#a9d6e5")

#axs.set_ylabel(r'$P(n_{agg})$',size=25)
#axs.set_ylabel("Inverse " r'$CDF(n_{agg})$',size=15)
axs.set_ylabel(r'$CDF(n_{agg})$',size=15)
axs.set_xlabel("Aggregate Size",size=15)
#axs.tick_params(axis='y', labelsize=15)
#axs.tick_params(axis='x', labelsize=15)
axs.legend(loc="upper right")
#axs.set_xticks(np.arange(1, 11, step=1))
axs.set_yticks(np.arange(0, 1.1, step=0.2))
plt.savefig("/media/jje63/easystore/Graphs/CDF_GNP_Core.pdf",format='pdf',dpi=500, bbox_inches='tight')"""



# =============================================================================
# """
# ### Largest Aggregat Fraction ###
# LC5OctAvg = [np.mean(LC5Oct[1])/20]
# LC5DodAvg = [np.mean(LC5Dod[1])/20]
# LC5HexAvg = [np.mean(LC5Hex[1])/20]
# LC5IcoAvg = [np.mean(LC5Ico[1])/20]
# LC5TetAvg = [np.mean(LC5Tet[1])/20]
# ### Monomer Fraction ###
# LC5OctAvg = [np.mean(LC5Oct[2])/20]
# LC5DodAvg = [np.mean(LC5Dod[2])/20]
# LC5HexAvg = [np.mean(LC5Hex[2])/20]
# LC5IcoAvg = [np.mean(LC5Ico[2])/20]
# LC5TetAvg = [np.mean(LC5Tet[2])/20]
# ### Average Size ###
# LC5OctAvg = [np.mean(LC5Oct[3])]
# LC5DodAvg = [np.mean(LC5Dod[3])]
# LC5HexAvg = [np.mean(LC5Hex[3])]
# LC5IcoAvg = [np.mean(LC5Ico[3])]
# LC5TetAvg = [np.mean(LC5Tet[3])]
# """
# 
# """
C5OctStd = np.std(C5OctAvg)
C5DodStd = np.std(C5DodAvg)
C5HexStd = np.std(C5HexAvg)
C5IcoStd = np.std(C5IcoAvg)
C5TetStd = np.std(C5TetAvg)
# 
P5OctStd = np.std(P5OctAvg)
P5DodStd = np.std(P5DodAvg)
P5HexStd = np.std(P5HexAvg)
P5IcoStd = np.std(P5IcoAvg)
P5TetStd = np.std(P5TetAvg)
# 
# SSOctStd = np.std(SSOctAvg)
# SSDodStd = np.std(SSDodAvg)
# SSHexStd = np.std(SSHexAvg)
# SSIcoStd = np.std(SSIcoAvg)
# SSTetStd = np.std(SSTetAvg)
# 
# 
AvgC5 = [np.mean(C5OctAvg), np.mean(C5DodAvg), np.mean(C5HexAvg), np.mean(C5IcoAvg), np.mean(C5TetAvg)]
stdC5 = [C5OctStd/math.sqrt(5),C5DodStd/math.sqrt(5),C5HexStd/math.sqrt(5),C5IcoStd/math.sqrt(5),C5TetStd/math.sqrt(5)]
print(AvgC5)
AvgP5 = [np.mean(P5OctAvg), np.mean(P5DodAvg), np.mean(P5HexAvg), np.mean(P5IcoAvg), np.mean(P5TetAvg)]
stdP5 = [P5OctStd/math.sqrt(6),P5DodStd/math.sqrt(6),P5HexStd/math.sqrt(6),P5IcoStd/math.sqrt(6),P5TetStd/math.sqrt(6)]
print(AvgP5)
# AvgSS = [np.mean(SSOctAvg), np.mean(SSDodAvg), np.mean(SSHexAvg), np.mean(SSIcoAvg), np.mean(SSTetAvg)]
# stdSS = [SSOctStd/math.sqrt(5),SSDodStd/math.sqrt(5),SSHexStd/math.sqrt(5),SSIcoStd/math.sqrt(5),SSTetStd/math.sqrt(5)]
# 
# #LAvgC5 = [np.mean(LC5OctAvg), np.mean(LC5DodAvg), np.mean(LC5HexAvg), np.mean(LC5IcoAvg), np.mean(LC5TetAvg)]
# 
figure , axs = plt.subplots(1, figsize=(8,6), sharex=True)
# figure.tight_layout(pad=2)
# axs.errorbar([2,3,4,5,6], AvgP5, yerr=stdP5,linestyle='solid',linewidth=3, marker='^',markersize = 13,capsize=8,color="#fc8900",label="Polar")
# axs.errorbar([2,3,4,5,6], AvgC5, yerr=stdC5, linestyle='solid',linewidth=3,marker='o',alpha=0.5,markersize = 13,capsize=8,color="#003dfc",label="Hydrophobic")
# axs.errorbar([2,3,4,5,6], AvgSS, yerr=stdSS, linestyle='solid',linewidth=3,marker='o',markersize = 13,capsize=8,color="grey",label="Soft Sphere")
# 
# #axs.plot([8,12,16,20,24], LAvgC5, linestyle='solid',linewidth=3,marker='o',alpha=0.5,color="#003dfc",markersize = 13,label="Hydrophobic")
# #axs.scatter([8,12,16,20,24], LAvgC5, linestyle='solid',linewidth=3,marker='o',alpha=0.5, s=40,color="#003dfc")
# axs.set_yticks(np.arange(0, 1.2, step=0.2))
# axs.tick_params(axis='y', labelsize=15)
# axs.tick_params(axis='x', labelsize=15)
# #axs.set_yticks(np.arange(0, 11, step=1))
# #axs.set_yticklabels(["$0.0$","$0.2$","$0.4$","$0.6$","$0.8$","$1.0$"],fontdict=font2)
# #axs.set_ylabel(r'$\langle F_{a} \rangle$',size=35)
# axs.set_ylabel(r'$\langle F_{m} \rangle$',size=35)
# #axs.set_ylabel(r'$\langle F_{s} \rangle$',fontdict=font)
# axs.set_xlabel('Ligand Length',size=25)
# #axs.legend(loc="lower right") #bbox_to_anchor=(1.0, 1.0)
# axs.legend(loc="upper right")
# plt.savefig("/media/jje63/easystore/Graphs/Fmonomerposter.pdf",format='pdf',dpi=500, bbox_inches='tight')
# #["(8-10)","(12-14)","(16-18)","(20-22)","(24-26)"]
# """
# =============================================================================

