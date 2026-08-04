# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 16:42:35 2022
@author: jahmalennis
"""
import math
S = str
F = float
I = int
def groAtom(a):
    #012345678901234567890123456789012345678901234567890
    #    1PRN      N    1   4.168  11.132   5.291
    ## ===>   atom name,   res name,     index, chain,       x,          y,          z       
    return (S(a[10:15]), S(a[5:10]),   I(a[16:20]), " ", F(a[20:28]),F(a[28:36]),F(a[36:44]))

class GoldBonder:
    def __init__(self, InputFile, OutputFile, BeadTypes, CutOffs, LigandType):
        self.atoms = []
        self.BeadTypes = BeadTypes
        self.CutOffs = CutOffs
        self.LigandType = LigandType
        self.InputFile = open(InputFile,'r')
        self.OutputFile = open(OutputFile, 'w')
        
    def TitleWriter(self, Title):
        
        if Title == "Main":
            self.OutputFile.write("%16s\n%1s%5s%18s\n%2s%19s\n\n%9s\n%1s%5s%11s%7s%8s%6s%8s%11s%11s\n"%(
                                  "[ moleculetype ]",";"," Name","nrexcl","AU","1","[ atoms ]",";","nr",
                                  "type","resnr","residue","atom","cgnr","charge","mass"))
        elif Title == "Bond":
            self.OutputFile.write("\n%10s\n%1s%10s%12s%9s%12s%10s\n"%("[ bonds ]",";","i","j",
                                                                    "funct","length","force_k"))
        
        elif Title == "Angle" and self.LigandType != 'butanethiol':
            self.OutputFile.write("\n%11s\n%1s%3s%2s%2s%10s%7s%10s\n"%("[ angles ]",";","i","j","k",
                                                                    "funct","angle","force.c."))   
    
    def growriter(self):
        lines = self.InputFile.readlines()
        self.atoms = [groAtom(i) for i in lines[2:-1]]
        self.InputFile.close()
        
    def BeadDefinition(self):
        self.TitleWriter("Main")
        for line in self.atoms:
            if line[0] in ['  AUC','  AUS','  AUL']:
                self.OutputFile.write("%6d%10s%6d%6s%8s%7d%10d%13d\n"%(line[2],self.BeadTypes[0],1,'AU', 
                                                                  line[1],line[2],0,784))
            elif line[0] == '  S  ':
                self.OutputFile.write("%6d%10s%6d%6s%8s%7d%10d%13d\n"%(line[2],self.BeadTypes[1],1,'AU', 
                                                                  "S    ",line[2],0,46))
            elif line[0] == '  C1 ':
                self.OutputFile.write("%6d%10s%6d%6s%8s%7d%10d%13d\n"%(line[2],self.BeadTypes[2],1,'AU', 
                                                                  "LIG  ",line[2],0,56))
            
            else:
                print(f"line {line[0]} is not defined, add bead to bead definition")
                print(line[0])
                break
                                                                                        
    def LigandAngle(self):
        self.TitleWriter("Angle")
        if self.LigandType == "dodecanethiol":
            for line in self.atoms:
                if line[0] == '  S  ':
                    numlis = [i for i in range(line[2], line[2]+4)]
                    self.OutputFile.write("%6d%5d%5d%4d%9.1f%6.1f\n%6d%5d%5d%4d%9.1f%6.1f\n"%(numlis[0],numlis[1],numlis[2],2,180.0,25.0,
                                                                                              numlis[1],numlis[2],numlis[3],2,180.0,25.0))
        elif self.LigandType == "octanethiol":
            for line in self.atoms:
                if line[0] == '  S  ':
                    numlis = [i for i in range(line[2], line[2]+3)]
                    self.OutputFile.write("%6d%5d%5d%4d%9.1f%6.1f\n"%(numlis[0],numlis[1],numlis[2],2,180.0,25.0))
       
        elif self.LigandType == "butanethiol":
            pass
                    
        elif self.LigandType == "hexadecanethiol":
            for line in self.atoms:
                if line[0] == '  S  ':
                    numlis = [i for i in range(line[2], line[2]+5)]
                    self.OutputFile.write("%6d%5d%5d%4d%9.1f%6.1f\n%6d%5d%5d%4d%9.1f%6.1f\n%6d%5d%5d%4d%9.1f%6.1f\n"%(numlis[0],numlis[1],numlis[2],2,180.0,25.0,
                                                                                                                      numlis[1],numlis[2],numlis[3],2,180.0,25.0,
                                                                                                                      numlis[2],numlis[3],numlis[4],2,180.0,25.0))        
        elif self.LigandType == "icosanethiol":
            for line in self.atoms:
                if line[0] in ['  S  ','    S']:
                    numlis = [i for i in range(line[2], line[2]+6)]
                    self.OutputFile.write("%6d%5d%5d%4d%9.1f%6.1f\n%6d%5d%5d%4d%9.1f%6.1f\n%6d%5d%5d%4d%9.1f%6.1f\n%6d%5d%5d%4d%9.1f%6.1f\n"%(numlis[0],numlis[1],numlis[2],2,180.0,25.0,
                                                                                                                                              numlis[1],numlis[2],numlis[3],2,180.0,25.0,
                                                                                                                                              numlis[2],numlis[3],numlis[4],2,180.0,25.0,
                                                                                                                                              numlis[3],numlis[4],numlis[5],2,180.0,25.0)) 
        elif self.LigandType == "tetracosanethiol":
            for line in self.atoms:
                if line[0] in ['  S  ','    S']:
                    numlis = [i for i in range(line[2], line[2]+7)]
                    self.OutputFile.write("%6d%5d%5d%4d%9.1f%6.1f\n%6d%5d%5d%4d%9.1f%6.1f\n%6d%5d%5d%4d%9.1f%6.1f\n%6d%5d%5d%4d%9.1f%6.1f\n%6d%5d%5d%4d%9.1f%6.1f\n"%(numlis[0],numlis[1],numlis[2],2,180.0,25.0,
                                                                                                                                                                      numlis[1],numlis[2],numlis[3],2,180.0,25.0,
                                                                                                                                                                      numlis[2],numlis[3],numlis[4],2,180.0,25.0,
                                                                                                                                                                      numlis[3],numlis[4],numlis[5],2,180.0,25.0,
                                                                                                                                                                      numlis[4],numlis[5],numlis[6],2,180.0,25.0))
    def BeadConnectivity(self):
        self.TitleWriter("Bond")
        for i in range(len(self.atoms) - 1):
            for j in range(len(self.atoms)):
                
                BeadDistance = math.sqrt((self.atoms[i][4] - self.atoms[j][4])**2 + 
                                         (self.atoms[i][5] - self.atoms[j][5])**2 + 
                                         (self.atoms[i][6] - self.atoms[j][6])**2)

                if self.atoms[i][0] == '  AUC' and self.atoms[j][0] == '  AUC' and i < j:
                    if BeadDistance < self.CutOffs[0]:
                        self.AUC_AUCCon(BeadDistance,self.atoms[i][2],self.atoms[j][2])
                elif self.atoms[i][0] == '  AUC' and self.atoms[j][0] == '  AUS' and i < j:
                    if BeadDistance < self.CutOffs[1]:
                        self.AUC_AUSCon(BeadDistance,self.atoms[i][2],self.atoms[j][2])
                elif self.atoms[i][0] == '  AUS' and self.atoms[j][0] == '  AUL' and i < j:
                    if BeadDistance < self.CutOffs[2]:
                        self.AUS_AULCon(BeadDistance,self.atoms[i][2],self.atoms[j][2])
                elif self.atoms[i][0] == '  AUSL' and self.atoms[j][0] == '  AUL' and i < j:
                    if BeadDistance < self.CutOffs[2]:
                        self.AUS_AULCon(BeadDistance,self.atoms[i][2],self.atoms[j][2])
                elif self.atoms[i][0] == '  AUL' and self.atoms[j][0] in ['  S  ', '    S'] and i < j:
                    if BeadDistance < self.CutOffs[2]:
                        self.AUS_AULCon(BeadDistance,self.atoms[i][2],self.atoms[j][2])
                elif self.atoms[i][0] == '  AUSL' and self.atoms[j][0] in ['  S  ', '    S'] and i < j:
                    if BeadDistance < .380:
                        self.S_SCon(BeadDistance,self.atoms[i][2],self.atoms[j][2])
                elif self.atoms[i][0] in ['  S  ', '    S'] and self.atoms[j][0] in ['  S  ','    S'] and i < j:
                    if BeadDistance < .430:
                        self.AUS_SCon(BeadDistance,self.atoms[i][2],self.atoms[j][2])
            if self.atoms[i][0] in ['  S  ','    S']: 
                if self.LigandType == "dodecanethiol":
                    numlis = [i for i in range(self.atoms[i][2], self.atoms[i][2]+5)]
                    self.dodecaneconnect(numlis)
                    
                elif self.LigandType == "hexadecanethiol":
                    numlis = [i for i in range(self.atoms[i][2], self.atoms[i][2]+6)]
                    self.hexadecaneconnect(numlis)
                    
                elif self.LigandType == "octanethiol":
                    numlis = [i for i in range(self.atoms[i][2], self.atoms[i][2]+4)]
                    self.octaneconnect(numlis)
                elif self.LigandType == "butanethiol":
                    numlis = [i for i in range(self.atoms[i][2], self.atoms[i][2]+3)]
                    self.butaneconnect(numlis)
                    
                elif self.LigandType == "icosanethiol":
                    numlis = [i for i in range(self.atoms[i][2], self.atoms[i][2]+7)]
                    self.icosaneconnect(numlis) 
                elif self.LigandType == "tetracosanethiol":
                    numlis = [i for i in range(self.atoms[i][2], self.atoms[i][2]+8)]
                    self.tetracosaneconnect(numlis)
                    
                else:
                    print(f"line {self.atoms[i][1]} ligand type is not defined, add ligand type to ligand definition")
                    
               
    def AUC_AUCCon(self,dist,index1,index2):
        self.OutputFile.write("%10d%11d%7d%16.3f%5d\n"%(index1,index2,1,dist,3500))
    def AUC_AUSCon(self,dist,index1,index2):
        self.OutputFile.write("%10d%11d%7d%16.3f%5d\n"%(index1,index2,1,dist,5000))
    def AUS_AULCon(self,dist,index1,index2):
        self.OutputFile.write("%10d%11d%7d%16.3f%5d\n"%(index1,index2,1,dist,5000))
    def AUS_SCon(self,dist,index1,index2):
        self.OutputFile.write("%10d%11d%7d%16.3f%5d\n"%(index1,index2,1,dist,1250))
    def S_SCon(self,dist,index1,index2):
        self.OutputFile.write("%10d%11d%7d%16.3f%5d\n"%(index1,index2,1,dist,1250))
 
## LIGAND TYPES ##
    def butaneconnect(self,num):
        self.OutputFile.write("%10d%11d%7d%16.3f%5d\n"%(num[0],num[1],1,.470,1250))
    def octaneconnect(self,num):
        self.OutputFile.write("%10d%11d%7d%16.3f%5d\n%10d%11d%7d%16.3f%5d\n"%(num[0],num[1],1,.470,1250,
                                                                              num[1],num[2],1,.470,1250,))
    def dodecaneconnect(self,num):
        self.OutputFile.write("%10d%11d%7d%16.3f%5d\n%10d%11d%7d%16.3f%5d\n%10d%11d%7d%16.3f%5d\n"%(num[0],num[1],1,.470,1250,
                                                                                                    num[1],num[2],1,.470,1250,
                                                                                                    num[2],num[3],1,.470,1250))
    def hexadecaneconnect(self,num):
        self.OutputFile.write("%10d%11d%7d%16.3f%5d\n%10d%11d%7d%16.3f%5d\n%10d%11d%7d%16.3f%5d\n%10d%11d%7d%16.3f%5d\n"%(num[0],num[1],1,.470,1250,
                                                                                                                          num[1],num[2],1,.470,1250,
                                                                                                                          num[2],num[3],1,.470,1250,
                                                                                                                          num[3],num[4],1,.470,1250))
    def icosaneconnect(self,num):
        self.OutputFile.write("%10d%11d%7d%16.3f%5d\n%10d%11d%7d%16.3f%5d\n%10d%11d%7d%16.3f%5d\n%10d%11d%7d%16.3f%5d\n%10d%11d%7d%16.3f%5d\n"%(num[0],num[1],1,.470,1250,
                                                                                                                                                num[1],num[2],1,.470,1250,
                                                                                                                                                num[2],num[3],1,.470,1250,
                                                                                                                                                num[3],num[4],1,.470,1250,
                                                                                                                                                num[4],num[5],1,.470,1250))
                                                                                                                                                
    def tetracosaneconnect(self,num):
        self.OutputFile.write("%10d%11d%7d%16.3f%5d\n%10d%11d%7d%16.3f%5d\n%10d%11d%7d%16.3f%5d\n%10d%11d%7d%16.3f%5d\n%10d%11d%7d%16.3f%5d\n%10d%11d%7d%16.3f%5d\n"%(num[0],num[1],1,.470,1250, 
        																			                                                                                  num[1],num[2],1,.470,1250, 
                                                                                                                                                                      num[2],num[3],1,.470,1250,
                                                                                                                                                                      num[3],num[4],1,.470,1250,
                                                                                                                                                                      num[4],num[5],1,.470,1250,
                                                                                                                                                                      num[5],num[6],1,.470,1250))                                                                                                                                          
## CENTRAL CONTROL ##    
    def ControlNano(self):
        self.growriter()
        self.BeadDefinition()
        self.BeadConnectivity()
        self.LigandAngle()
        self.OutputFile.close()
