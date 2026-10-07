#!/bin/bash

puts "Processing File"
set empath [lindex $argv 0]
mol new $empath waitfor all
mol addfile center.xtc waitfor all

source ../../../../Figure_1/SASA.tcl
source ../../../../Figure_1/measurecontact.tcl

solventaccessible "resname AU POPC" "name AUC AUSL AUL" 2.64 0 -1 analysis/watersasa
solventaccessible "resname AU W ION" "name AUC AUSL AUL" 2.64 0 -1 analysis/lipidsasa

measureContact "name C1A D2A C3A C4A C1B C2B C3B C4B" "name AUC AUSL AUL" 8 0 -1 analysis/tailcont
measureContact "name NC3 PO4 GL1 GL2" "name AUC AUSL AUL" 8 0 -1 analysis/headcont
