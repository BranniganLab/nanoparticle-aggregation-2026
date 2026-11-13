#!/bin/bash

# Setup and download from zenodo
if command -v gmx &> /dev/null; then
    echo "✅ GROMACS is accessible."
    gmx --version | grep "GROMACS version" # Optional: print the version
else
    echo "❌ GROMACS (gmx) could not be found."
    echo "Please ensure GROMACS is installed or source your 'GMXRC' file."
    exit 1
fi

if command -v vmd &> /dev/null; then
    echo "VMD is installed: $(command -v vmd)"
else
    echo "Error: VMD is not installed or not found in PATH." >&2
    exit 1
fi

SECONDS=0

echo "Beginning analysis..." 
cd Figure_1
bash SASA.sh
cd ../Figure_2 
bash Distance_umbsamp.sh
cd ../Figure_3
bash cluster_all.sh
cd ../

echo "Beginning plotting....."
python ../Figure_Making_Scripts/Figure1.py -fs
python ../Figure_Making_Scripts/Figure2.py -fs
python ../Figure_Making_Scripts/Figure3.py -fs
python ../Figure_Making_Scripts/SF1.py -fs
python ../Figure_Making_Scripts/SF2.py -fs
python ../Figure_Making_Scripts/SF3.py -fs

echo "Script finished in $((SECONDS / 3600)) hours."
