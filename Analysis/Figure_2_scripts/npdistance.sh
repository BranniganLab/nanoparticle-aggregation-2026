echo "selection 1 $1"
echo "selection 2 $2"
i=0
mkdir NPdistance
cd NPdistance
for file in $(ls ../umbrella*.xtc | sort -V); do
	basename_only="${file%.*}"
	tprfile="$basename_only.tpr"
	xtcfile="$file"
	echo $tprfile
	echo $xtcfile	
  	i=$((i + 1))
  	gmx distance -f $xtcfile -s $tprfile -select "com of group $1 plus com of group $2" -oxyz distance_components_$i.xvg -n ../index.ndx
done