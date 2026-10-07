#!/bin/bash

echo "selection 1 $1"
echo "selection 2 $2"
echo "index path $3"
i=0

if [[ -d "NPdistance" ]]; then
    echo "NPdistance folder exist"
else
    echo "Making NPdistance folder"
    mkdir NPdistance
fi

cd NPdistance
for file in $(ls ../umbrella*.xtc | sort -V); do
	basename_only="${file%.*}"
	clean_basename="${basename_only//..\//}"
	tprfile="$3/$clean_basename.tpr"
	xtcfile="$file"
	echo $tprfile
	echo $xtcfile	
  	i=$((i + 1))
  	gmx distance -f $xtcfile -s $tprfile -select "com of group $1 plus com of group $2" -oxyz distance_components_$i.xvg -n "$3/index.ndx"
  	gmx mdrun -s $tprfile -rerun $xtcfile -pf "../$clean_basename"_pullf.xvg"" -px "../$clean_basename"_pullx.xvg"" -e "../$clean_basename".edr""
done