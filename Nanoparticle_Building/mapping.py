#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 28 09:28:09 2021

@author: jahmalennis
"""
S = str
F = float
I = int
Atomlist = ['  AUC','  AUS','  AUL','   S1','  H11','  H13','  H22','  H21','  H23','   C1','   C2'] 
def groAtom(a):
    #012345678901234567890123456789012345678901234567890
    #    1PRN      N    1   4.168  11.132   5.291
    ## ===>   atom name,   res name,     index, chain,       x,          y,          z       
    return (S(a[10:15]), S(a[5:10]),   I(a[16:20]), " ", F(a[20:28]),F(a[28:36]),F(a[36:44]))

class MappingStructure:    
    def __init__(self, InputFile, OutputFile, ligandtype):
        self.atoms = []
        self.rest = []
        self.InputFile = open(InputFile,'r')
        self.OutputFile = open(OutputFile, 'w')
        self.ligandtype = ligandtype

## MAPPING CONTROLS ##

    def growriter(self):
        lines = self.InputFile.readlines()
        self.atoms = [groAtom(i) for i in lines[2:-1]]
        self.rest = [lines[0],lines[1],lines[-1]]
        self.InputFile.close()
            
    def beadmap(self):
        for line in self.atoms:
            if line[0] in ['  AUC','  AUS','  AUL']:
               self.goldbeads(line[2])
            
            elif line[0] == '   S1':
              self.sulfurbeads(line[2])
            
            elif line[0] == '  H22':
                if self.ligandtype == "dodecanethiol":
                    self.dodecanethiol(line[2])
                elif self.ligandtype == "butanethiol":
                    self.butanethiol(line[2])
                elif self.ligandtype == "octanethiol":
                    self.octanethiol(line[2])
                elif self.ligandtype == "hexadecanethiol":
                    self.hexadecanethiol(line[2])
                elif self.ligandtype == "icosanethiol":
                    self.icosanethiol(line[2])
                elif self.ligandtype == "tetracosanethiol":
                    self.tetracosanethiol(line[2])
                else:
                    print("Error:Ligand type not recognized, add ligand to ligand list")
            elif line[0] not in Atomlist:
                print(f"Error: line {line[0]} is not a known atom and will be excluded from mapping")

## MAPPING FOR EACH TYPE OF GOLD BEAD ##
    
    def goldbeads(self, num):
        self.OutputFile.write("[Bead {}]\n".format(num))
        self.OutputFile.write("%5d\n"%(num))
    
    def sulfurbeads(self, num):
        numlis = [i for i in range(num-3, num+1)]
        self.OutputFile.write("[Bead {}]\n".format(numlis[0]))
        self.OutputFile.write("%5d%5d%5d%5d\n"%(numlis[0],numlis[1],numlis[2],numlis[3]))

## MAPPING FOR DIFFERENT TYPES OF LIGANDS ##
    
    def butanethiol(self,num):
        numlis = [i for i in range(num-10, num+3)]
        if len(numlis) != 13:
            print(f"ERROR: line {num} does not fit within normal octanethiol ligand scheme")
        counter = 0
        holdlis = []
        for number in numlis:
            if counter == 11:
                holdlis.append(number)
                self.OutputFile.write("[Bead {}]\n".format(holdlis[0]))
                self.OutputFile.write("%5d%5d%5d%5d%5d%5d%5d%5d%5d%5d%5d%5d\n"%(holdlis[0],holdlis[1],holdlis[2],
                                                                                holdlis[3],holdlis[4],holdlis[5],
                                                                                holdlis[6],holdlis[7],holdlis[8],
                                                                                holdlis[9],holdlis[10],holdlis[11]))
                holdlis = []
                counter = 0
            else:
                holdlis.append(number)
                counter += 1
    
    
    def octanethiol(self,num):
        numlis = [i for i in range(num-22, num+3)]
        if len(numlis) != 25:
            print(f"ERROR: line {num} does not fit within normal octanethiol ligand scheme")
        counter = 0
        holdlis = []
        for number in numlis:
            if counter == 11:
                holdlis.append(number)
                self.OutputFile.write("[Bead {}]\n".format(holdlis[0]))
                self.OutputFile.write("%5d%5d%5d%5d%5d%5d%5d%5d%5d%5d%5d%5d\n"%(holdlis[0],holdlis[1],holdlis[2],
                                                                                holdlis[3],holdlis[4],holdlis[5],
                                                                                holdlis[6],holdlis[7],holdlis[8],
                                                                                holdlis[9],holdlis[10],holdlis[11]))
                holdlis = []
                counter = 0
            else:
                holdlis.append(number)
                counter += 1
                
    def dodecanethiol(self,num):
        numlis = [i for i in range(num-34, num+3)]
        if len(numlis) != 37:
            print(f"ERROR: line {num} does not fit within normal dodecanethiol ligand scheme")
        counter = 0
        holdlis = []
        for number in numlis:
            if counter == 11:
                holdlis.append(number)
                self.OutputFile.write("[Bead {}]\n".format(holdlis[0]))
                self.OutputFile.write("%5d%5d%5d%5d%5d%5d%5d%5d%5d%5d%5d%5d\n"%(holdlis[0],holdlis[1],holdlis[2],
                                                                                holdlis[3],holdlis[4],holdlis[5],
                                                                                holdlis[6],holdlis[7],holdlis[8],
                                                                                holdlis[9],holdlis[10],holdlis[11]))
                holdlis = []
                counter = 0
            else:
                holdlis.append(number)
                counter += 1
                
    def hexadecanethiol(self,num):
        numlis = [i for i in range(num-46, num+3)]
        if len(numlis) != 49:
            print(f"ERROR: line {num} does not fit within normal hexadecanethiol ligand scheme")
        counter = 0
        holdlis = []
        for number in numlis:
            if counter == 11:
                holdlis.append(number)
                self.OutputFile.write("[Bead {}]\n".format(holdlis[0]))
                self.OutputFile.write("%5d%5d%5d%5d%5d%5d%5d%5d%5d%5d%5d%5d\n"%(holdlis[0],holdlis[1],holdlis[2],
                                                                                holdlis[3],holdlis[4],holdlis[5],
                                                                                holdlis[6],holdlis[7],holdlis[8],
                                                                                holdlis[9],holdlis[10],holdlis[11]))
                holdlis = []
                counter = 0
            else:
                holdlis.append(number)
                counter += 1
    
    def icosanethiol(self,num):
        numlis = [i for i in range(num-58, num+3)]
        if len(numlis) != 61:
            print(f"ERROR: line {num} does not fit within normal icosanethiol ligand scheme")
        counter = 0
        holdlis = []
        for number in numlis:
            if counter == 11:
                holdlis.append(number)
                self.OutputFile.write("[Bead {}]\n".format(holdlis[0]))
                self.OutputFile.write("%5d%5d%5d%5d%5d%5d%5d%5d%5d%5d%5d%5d\n"%(holdlis[0],holdlis[1],holdlis[2],
                                                                                holdlis[3],holdlis[4],holdlis[5],
                                                                                holdlis[6],holdlis[7],holdlis[8],
                                                                                holdlis[9],holdlis[10],holdlis[11]))
                holdlis = []
                counter = 0
            else:
                holdlis.append(number)
                counter += 1
    def tetracosanethiol(self,num):
        numlis = [i for i in range(num-70, num+3)]
        if len(numlis) != 73:
            print(f"ERROR: line {num} does not fit within normal tetracosanethiol ligand scheme")
        counter = 0
        holdlis = []
        for number in numlis:
            if counter == 11:
                holdlis.append(number)
                self.OutputFile.write("[Bead {}]\n".format(holdlis[0]))
                self.OutputFile.write("%5d%5d%5d%5d%5d%5d%5d%5d%5d%5d%5d%5d\n"%(holdlis[0],holdlis[1],holdlis[2],
                                                                                holdlis[3],holdlis[4],holdlis[5],
                                                                                holdlis[6],holdlis[7],holdlis[8],
                                                                                holdlis[9],holdlis[10],holdlis[11]))
                holdlis = []
                holdlis = []
                counter = 0
            else:
                holdlis.append(number)
                counter += 1
## CENTRAL CONTROL COMMAND ##
    def controlmap(self):
        self.growriter()
        self.beadmap()
        self.OutputFile.close()
     
                    
