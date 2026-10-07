#!/bin/bash

CWD=`pwd`
echo "IN DIRECTORY: $CWD"
hydropath="Multi_Nanoparticle/10_NP_Systems/Hydrophobic/"
cd "../$hydropath"
for dir in *thiol/; do
    dir_name="${dir%/}"
    echo "Processing directory: $dir"
    cd $dir
    for rep_dir in Replica_*[1-5]; do
    	cd $rep_dir
        relpath="../../../../../../Simulation/$hydropath$dir$rep_dir/setup/em.gro"
        echo $relpath 
        if [[ -d "analysis" ]]; then
            echo "Analysis folder exist"
        else
            echo "Making Analysis folder"
            mkdir analysis
        fi
    	echo "Processing directory: $rep_dir"
    	vmd2 -dispdev text -eofexit < $CWD/cluster_all.tcl $relpath > fullclus.log
    	cd ../
    done
    cd ../
done

cd $CWD
polarpath="Multi_Nanoparticle/10_NP_Systems/Polar/"
cd "../$polarpath"
for dir in *thiol/; do
    dir_name="${dir%/}"
    echo "Processing directory: $dir"
    cd $dir
    for rep_dir in Replica_*[1-5]; do
        cd $rep_dir
        relpath="../../../../../../Simulation/$polarpath$dir$rep_dir/setup/em.gro"
        echo $relpath 
        if [[ -d "analysis" ]]; then
            echo "Analysis folder exist"
        else
            echo "Making Analysis folder"
            mkdir analysis
        fi
        echo "Processing directory: $rep_dir"
        vmd2 -dispdev text -eofexit < $CWD/cluster_all.tcl $relpath > fullclus.log
        cd ../
    done
    cd ../
done

cd $CWD
sspath="Multi_Nanoparticle/10_NP_Systems/Soft_Sphere/"
cd "../$sspath"
for dir in *thiol/; do
    dir_name="${dir%/}"
    echo "Processing directory: $dir"
    cd $dir
    for rep_dir in Replica_*[1-5]; do
        cd $rep_dir
        relpath="../../../../../../Simulation/$sspath$dir$rep_dir/setup/em.gro"
        echo $relpath 
        if [[ -d "analysis" ]]; then
            echo "Analysis folder exist"
        else
            echo "Making Analysis folder"
            mkdir analysis
        fi
        echo "Processing directory: $rep_dir"
        vmd2 -dispdev text -eofexit < $CWD/cluster_all.tcl $relpath > fullclus.log
        cd ../
    done
    cd ../
done

cd $CWD
