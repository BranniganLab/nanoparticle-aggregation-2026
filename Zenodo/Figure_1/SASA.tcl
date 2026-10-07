proc average L {
    expr ([join $L +])/[llength $L].
}

# solventaccessible --
#		Finds solvent accesible surface area restricted to RestrictedText but including all SelectionText
#
# Arguments:
#		SelectionText		(Str)   Selection for SASA and areas you don't want to include as solvent
#		RestrictedText		(Str)   Selection for SASA
#		ShellRadius			(Float) Radius for the SASA search
#		StartFrame			(Int)	Starting Frame for analysis
#		EndFrame			(Int)	End Frame for analysis
#		FileName			(Str)	Name of the file to put SASA data
#
# Results:
#		File with frame and solvent accesible surface area of RestrictedText
proc solventaccessible {SelectionText RestrictedText ShellRadius StartFrame EndFrame FileName} {
	set sel [atomselect top $SelectionText]
	set sel2 [atomselect top $RestrictedText]
	set File1 [open "$FileName.dat" w+]
	puts $File1 "# Selection:$SelectionText Restricted:$RestrictedText Radius:$ShellRadius Start:$StartFrame End:$EndFrame"
	if {$EndFrame == -1} {
		set EndFrame [molinfo top get numframes]
	}   
	for {set j $StartFrame} {$j <= $EndFrame} {incr j} {
		$sel frame $j
		$sel2 frame $j
		$sel update
		$sel2 update
		set SASA [measure sasa $ShellRadius $sel -restrict $sel2]
		puts $File1 "$j $SASA"
		puts "Finished Frame: $j"
	}
	$sel delete
	$sel2 delete
	close $File1
}

# multinanoSASA --
#		Finds Solvent accesible surface area for all molecules in selection (based on resid)
#
# Arguments:
#		NPSelection			(Str)   Resname of molecule selection
#		cutoff				(Float) Shell Radius for sasa analysis
#
# Results:
#		Multiple files each containing the SASA for a single molecule in selection 
proc multinanoSASA {NPSelection {cutoff 2.5}} {
	set sel [atomselect top "resname $NPSelection"]
	set NpList [lsort -unique -integer [$sel get resid]]
	puts "Returning Values for Nanoparticles: $NpList"
	$sel delete
	for {set i [lindex $NpList 0]} {$i <= [lindex $NpList end]} {incr i} {
		if {$i < 10} {
			solventaccessible "resname $NPSelection and resid $i" $cutoff 250 -1 SASA0$i
		} else {
			solventaccessible "resname $NPSelection and resid $i" $cutoff 250 -1 SASA$i
		}
		puts "Nanoparticle $i is done"
	}

}

# showpoints --
#		Shows all sasa points for a single frame, must run vmd's SASA command and use the -points flag
#
# Arguments:
#		SASApoints		(List) list of points from vmd's SASA command
#
# Results:
#		Draws solvent accesible surface on molecule
proc showpoints {SASApoints} {
	foreach vec $SASApoints {
		graphics top color iceblue
		graphics top sphere $vec radius 2.6 resolution 20
	} 
	return
}

# rgyrtotal --
#		radius of gyration calculated by vmd
# 
# Arguments:
#		SelectionText 		(string) atomselection for radius of gyration measurment
#		StartFrame			(Int)	Starting Frame for analysis
#		EndFrame			(Int)	End Frame for analysis
#
# Result:
#		Calculates average radius of gyration
proc rgyrtotal {SelectionText StartFrame EndFrame} {
	set sel [atomselect top $SelectionText]
	set lis {}
	if {$EndFrame == -1} {
		set EndFrame [molinfo top get numframes]
	}   
	for {set j $StartFrame} {$j <= $EndFrame} {incr j} {
		$sel frame $j
		$sel update
		set rgyr [measure rgyr $sel weight none]
		lappend lis $rgyr
	}
	puts [average $lis]
}

# rgyrtotal --
#		radius of gyration calculated by vmd
# 
# Arguments:
#		SelectionText 		(string) atomselection for radius of gyration measurment
#		StartFrame			(Int)	Starting Frame for analysis
#		EndFrame			(Int)	End Frame for analysis
#
# Result:
#		Calculates average radius of gyration
proc rgyrframe {SelectionText StartFrame EndFrame FileName} {
	set sel [atomselect top $SelectionText]
	set File1 [open "$FileName.dat" w+]
	if {$EndFrame == -1} {
		set EndFrame [molinfo top get numframes]
	}   
	for {set j $StartFrame} {$j <= $EndFrame} {incr j} {
		$sel frame $j
		$sel update
		set rgyr [measure rgyr $sel weight none]
		puts $File1 "$j $rgyr"
		puts "Finished Frame: $j"
	}
	$sel delete
	close $File1

}
