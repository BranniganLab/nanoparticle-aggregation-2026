#!/bin/bash

CWD=`pwd`
echo $1

dimerpath="/Multi_Nanoparticle/Dimer_Free_Energy_System"
cd "../$dimerpath"
for dir in *; do
    dir_name="${dir%/}"
    echo "Processing directory: $dir"
    cd $dir
    if [ $dir == "Hydrophobic" ]; then
        P1="../../../../Helper/tpr-files_hyd.dat"
        if [ $1 == "no-hyd" ]; then
           cd ../
           continue 
        fi
    elif [ $dir == "Polar" ]; then
        P1="../../../../Helper/tpr-files_pol.dat"
        if [ $1 == "no-pol" ]; then
           cd ../
           continue
        fi
    elif [ $dir != "Hydrophobic" ] | [ $dir != "Polar" ]; then
        cd ../
        continue
    fi

    for rep_dir in Replica*[1-3]; do
        echo "CD dir: `pwd`"
    	cd $rep_dir
        relpath="../../../../../../Simulation$dimerpath/$dir_name/$rep_dir"
        echo $relpath 
    	echo "Processing directory: $rep_dir"
    	bash $CWD/npdistance.sh AUCORE1 AUCORE2 $relpath
        rm NPdistance/*.log*
        gmx wham -it $P1 -if ../../../../Helper/pullf-files.dat -o -hist 
    	cd ../
        echo "IN DIRECTORY: `pwd`"
    done
    cd ../
done
cd ../
