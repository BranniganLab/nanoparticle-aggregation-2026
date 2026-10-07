#!/bin/bash

CWD=`pwd`

snppath="Single_Nanoparticle/"
cd "../$snppath"
for dir in *; do
	echo $dir
    dir_name="${dir%/}"
    echo "Processing directory: $dir"
    cd $dir
    for thiol in *thiol; do
	    thiol_name="${thiol%/}"
	    echo "Processing directory: $dir"
	    cd $thiol
	    for rep_dir in Replica*[1-3]; do
	    	cd $rep_dir
	    	last_char="${rep_dir: -1}"
	        relpath="../../../../../Simulation/$snppath$dir_name/$thiol_name/Replica$last_char/em/em1.gro"
	        echo $relpath 
	        if [[ -d "analysis" ]]; then
	            echo "Analysis folder exist"
	        else
	            echo "Making Analysis folder"
	            mkdir analysis
	        fi
	    	echo "Processing directory: $rep_dir"
	    	vmd2 -dispdev text -eofexit < $CWD/sasa_contact.tcl $relpath > sasa_cont.log
	    	cd ../
	    done
	    cd ../
	done
	cd ../
done