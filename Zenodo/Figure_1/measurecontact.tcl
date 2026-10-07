# measureContact --
#		Finds contacts between two selections over frames
#
# Arguments:
#		SelectionText1		(Str)   Selection for SASA and areas you don't want to include as solvent
#		SelectionText2		(Str)   Selection for SASA
#		ShellRadius			(Float) Radius for the SASA search
#		StartFrame			(Int)	Starting Frame for analysis
#		EndFrame			(Int)	End Frame for analysis
#		FileName			(Str)	Name of the file to put SASA data
#
# Results:
#		File with frame and solvent accesible surface area of RestrictedText
proc measureContact {SelectionText1 SelectionText2 Cutoff StartFrame EndFrame FileName} {
	set sel [atomselect top $SelectionText1]
	set sel2 [atomselect top $SelectionText2]
	set File1 [open "$FileName.dat" w+]
	puts $File1 "# Selection 1:$SelectionText1 Selection 2:$SelectionText2 Cutoff:$Cutoff Start:$StartFrame End:$EndFrame"
	if {$EndFrame == -1} {
		set EndFrame [molinfo top get numframes]
	}   
	for {set j $StartFrame} {$j <= $EndFrame} {incr j} {
		$sel frame $j
		$sel2 frame $j
		$sel update
		$sel2 update
		set CONTACT [llength [lsort -unique [lindex [measure contacts $Cutoff $sel $sel2] 0]]]
		puts $File1 "$j $CONTACT"
		puts "Finished Frame: $j"
	}
	$sel delete
	$sel2 delete
	close $File1
}
