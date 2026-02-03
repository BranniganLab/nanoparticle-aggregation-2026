#!/bin/bash


for dir in Common_*[1-5]/; do
    dir_name="${dir%/}"
    echo "Processing directory: $dir"
    cd $dir
    for thiol_dir in */; do
    	cd $thiol_dir
    	echo "Processing directory: $thiol_dir"
    	vmd2 -dispdev text -eofexit < /home/jje63/Documents/Github_Repos/Martini_GNP_Paper/Analysis/Extra_scripts/cluster_all.tcl > fullclus.log
    	cd ../
    done
    cd ../
done

for dir in PolarNP_[1-5]/; do
    dir_name="${dir%/}"
    echo "Processing directory: $dir"
    cd $dir
    for thiol_dir in */; do
    	cd $thiol_dir
    	echo "Processing directory: $thiol_dir"
    	vmd2 -dispdev text -eofexit < /home/jje63/Documents/Github_Repos/Martini_GNP_Paper/Analysis/Extra_scripts/cluster_all.tcl > fullclus.log
    	cd ../
    done
    cd ../
done

for dir in Soft_Sphere_[1-5]/; do
    dir_name="${dir%/}"
    echo "Processing directory: $dir"
    cd $dir
    for thiol_dir in */; do
    	cd $thiol_dir
    	echo "Processing directory: $thiol_dir"
    	vmd2 -dispdev text -eofexit < /home/jje63/Documents/Github_Repos/Martini_GNP_Paper/Analysis/Extra_scripts/cluster_all.tcl > fullclus.log
    	cd ../
    done
    cd ../
done
