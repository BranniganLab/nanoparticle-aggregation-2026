#FindCluster --
#       Finds clusters of molecules within cutoff distance. 
#
#Arguments:
#       Data          (list)list of all molecule resid's 
#       CutOff        (Int)cutoff distance for single group of nanoparticles
#       MinPoint      (Int)Minimun number of molecules around a molecule for the
#                          molecule to be considered a cluster and not a noise point
#       MoleculeName  (String)Atomselection of resnames of molecules in cluster 
#        
#Results: 
#       The result returns a nested list of resid's of single molecules and molecules in 
#       a cluster 
#       ex. {{2 5} {{1 0 3 0 6 0 0 0 0 0} {0 0 0 4 0 0 7 8 9 10}}}
#         (Single)|                  (Clusters)
proc FindCluster { Data CutOff MinPoint MoleculeName Frm } {
        set NoisePoints {}
        set ClusterPoints {}
        set Counter 0
        foreach ResID $Data {
                if {[lsearch -index $Counter -all -inline $ClusterPoints $ResID]==""} {
                        if {[lsearch -inline $NoisePoints $ResID]==""} {
                                set NeighborPoints [FindNeighbors $MoleculeName $CutOff $ResID $Frm]
                                if {[llength $NeighborPoints] < $MinPoint} {
                                        lappend NoisePoints $ResID 
                                } else {
                                        set ClusterList [lrepeat [expr [llength $Data]] 0] 
                                        lappend ClusterPoints [ExpandCluster $ResID $NeighborPoints $CutOff $MinPoint $MoleculeName $ClusterList $Frm 0 $Data]
                                }
                        }
                }
                incr Counter 
        } 
        return [list $NoisePoints $ClusterPoints]
}

#ExpandCluster --
#       Finds all nanoparticles in a single cluster using a DBScan Alogrithim
#
#Arguments:
#       ResID           (Int)Resid of current molecule 
#       NeighborPoints  (list)list of resids of neighbors within cutoff distance
#       CutOff          (Int)(Int)cutoff distance for single group of nanoparticles
#       MinPoint        (Int)Minimun number of molecules around a molecule for the
#                            molecule to be considered a cluster and not a noise point
#       MoleculeName    (String)Atomselection of resnames of molecules in cluster
#       ClusterList     (List)list to hold all values of in the cluster. list is 
#                             initialized as empty list ex. {0 0 0 0 0}
#
#Results:
#       A list of resids of the nanoparticles inside of a single cluster
#       ex. {0 0 0 4 0 0 7 8 9 10} non zero values are part of cluster
proc ExpandCluster { ResID NeighborPoints CutOff MinPoint MoleculeName ClusterList Frm Counter Data } {
        if {[ListChecker $NeighborPoints $ClusterList] == False && $Counter != [expr [llength $Data]]} {
                foreach Neighbor $NeighborPoints {
                        set ClusterList [lreplace $ClusterList [expr $Neighbor-1] [expr $Neighbor-1] $Neighbor]
                        } 

                set ResID [lrange $NeighborPoints 1 end]
                set NeighborPoints [FindNeighbors $MoleculeName $CutOff $ResID $Frm]
                set Counter [expr $Counter + 1]
                return [ExpandCluster $ResID $NeighborPoints $CutOff $MinPoint $MoleculeName $ClusterList $Frm $Counter $Data]
        } else {
                return $ClusterList

        }
}

#FindNeighbors --
#       Finds all unique resids of atomselection within cutoff
#
#Arguments:
#       MoleculeName    (String)Atomselection of resnames of molecules in cluster
#       CutOff          (Int)(Int)cutoff distance for single group of nanoparticles
#       ResID           (Int)Resid of current molecule
#
#Results:
#       A list of all unique molecule resid's within the cutoff of a single molecule 
#       ex. {1 4 5}
#       (resid's around resid 4)
proc FindNeighbors { MoleculeName CutOff ResID Frm } {
        set sel [atomselect top "resname $MoleculeName and pbwithin $CutOff of (resname $MoleculeName and resid $ResID)" frame $Frm]
        set NeighborPoints [lsort -unique -integer [$sel get resid]]
        $sel delete
        return $NeighborPoints
}

#ListChecker --
#       Checks if all elements in list 1 are in list 2
#
#Arguments:
#       List1           (list)list of values 
#       List2           (list)list of values
#
#Result:
#       retuns true if all elements in list 1 are in list 2 and false
#       if all elements in list 1 are not in list 2
proc ListChecker {List1 List2} {
        foreach Element $List1 {
                if {$Element ni $List2} {
                        return False
                }
        }
        return True
}


#ClusterControl --
#       Writes cluster information to file for specified frames
#
#Arguments:
#       MoleculeName    (String)Atomselection of resnames of molecules in cluster
#       CutOff          (Int)cutoff distance for single group of nanoparticles
#       MinPoint        (Int)Minimun number of molecules around a molecule for the
#                            molecule to be considered a cluster and not a noise point
#       StartFrame      (Int)First frame to be analyzed
#       EndFrame        (Int)Last frame to be analyzed (if set to -1 then last frame 
#                            will be end of loaded frames)   
proc ClusterControl { MoleculeName CutOff MinPoint StartFrame EndFrame {name "Cluster"} } {
        set Clusterfile [open "$name$MoleculeName$CutOff.dat" w]
        set Data [lsort -unique -integer [[atomselect top "resname $MoleculeName" frame 0] get resid]]
        if {$EndFrame == -1} {
                set EndFrame [molinfo top get numframes]
        } 
        for {set frm $StartFrame} {$frm < $EndFrame} {incr frm} {
                puts "frame $frm"
                set ClusterValues [FindCluster $Data $CutOff $MinPoint $MoleculeName $frm]
                puts $Clusterfile "$frm [list [lindex $ClusterValues 0]] [list [lindex $ClusterValues 1]]"
        }
        close $Clusterfile
}

#findLargestAggregate --
#       Finds all the resid's of the molecules in the largest aggregate
#
#Arguments:
#       MoleculeName     (String)Atomselection of resnames of molecules in cluster
#       CutOff           (Int)(Int)cutoff distance for single group of nanoparticles
#       MinPoint         (Int)Minimun number of molecules around a molecule for the
#                             molecule to be considered a cluster and not a noise point
#       Frame            (Int)Frame being analyzed
#Results: 
#       Returns a list of the resid's in the largest aggregate
proc findLargestCluster { MoleculeName CutOff MinPoint Frame } {
        set Data [lsort -unique -integer [[atomselect top "resname $MoleculeName" frame 0] get resid]]
        set ClusterValues [FindCluster $Data $CutOff $MinPoint $MoleculeName $Frame]
        if {[llength [lindex $ClusterValues 1]] > 0} {
                set fewestZero [llength [lsearch -all [lindex $ClusterValues 1 0] 0]]
                set clusterResid [lindex $ClusterValues 1 0]
                foreach lisElem [lindex $ClusterValues 1] {
                        set zeroValues [llength [lsearch -all $lisElem 0]] 
                        if {$zeroValues < $fewestZero} {
                                set fewestZero $zeroValues
                                set clusterResid $lisElem 
                                }
                        }
        } else {
                return [list -1 [lindex $ClusterValues 0]]
        }
        return [list $fewestZero $clusterResid]
}

#calculatedRadiusOfGyration --
#
#Arguments:
#       MoleculeName     (String)Atomselection of resnames of molecules in cluster
#       CutOff           (Int)(Int)cutoff distance for single group of nanoparticles
#       MinPoint         (Int)Minimun number of molecules around a molecule for the
#                             molecule to be considered a cluster and not a noise point
#       Frame            (Int)Frame being analyzed
#Results: 
#       Returns the radius of gyration 
proc calculateRadiusOfGyration { MoleculeName CutOff MinPoint Frame } {
        set RID [findLargestCluster $MoleculeName $CutOff $MinPoint $Frame]
        if {[lindex $RID 1] != {}} {
                set RIDList [lindex $RID 1]
                set sel [atomselect top "resname $MoleculeName and resid $RIDList" frame $Frame]
                set RGYR [measure rgyr $sel weight none]
                
                $sel delete
                return $RGYR

        } else {
                puts "No Clusters Exist"
                return 0

        }
        return $fullRGYR
}


proc rgyrControl { MoleculeName CutOff MinPoint StartFrame EndFrame } {
        set rgyrfile [open "rgyrcluster$MoleculeName$CutOff.dat" w]
        if {$EndFrame == -1} {
                set EndFrame [molinfo top get numframes]
        } 
        for {set frm $StartFrame} {$frm < $EndFrame} {incr frm} {
                puts "frame $frm"
                set rgyrValues [calculateRadiusOfGyration $MoleculeName $CutOff $MinPoint $frm]
                puts $rgyrfile "$frm $rgyrValues"
        }
        close $rgyrfile
}

#### Need To Fix These ####
proc rgyrControlSpecial { StartFrame EndFrame } {
        set rgyrfile [open "rgyrclusterAU10.dat" w]
        if {$EndFrame == -1} {
                set EndFrame [molinfo top get numframes]
        } 
        set sel [atomselect top all]
        for {set frm $StartFrame} {$frm < $EndFrame} {incr frm} {
                puts "frame $frm"
                $sel frame $frm
                $sel update  
                set RGYR [measure rgyr $sel weight none]
                puts $rgyrfile "$frm $RGYR"
        }
        $sel delete
        close $rgyrfile
}


#### Need To Fix These ####


#proc colorchanger {residlis} {
## Controls cluster coloring 
#Variable
        #residlis: nested list of resid's in clusters ex. {{1 2 3} {2 3} 6} 
##
#       line 1-2: gets frame number and initializes k
#        upvar 1 frm frms
#        set k 0
#       line 3-4: loops through resid list
#        for {set t 0} {$t < [llength $residlis]} {incr t} {
#       line 5-7: Checks if nested list is empty list, sets atom selection to resid's, goes to proper frame 
#                if {[lindex $residlis $t]!= {}} {
#                        set sel [atomselect top "resid [lindex $residlis $t]"]
#                        animate goto $frms
#       line 8-10: Puts atom selection in proper frame, gives a color scale value to cluster, adds 5 to value to increase color diference
#                        $sel frame $frms
#                        $sel set user $t 
#       line 11-12: deletes atom selection and modifies colors of molecule on screen
#                        $sel delete
#                        mol modcolor 0 0 User
#                } 
#        }
#}