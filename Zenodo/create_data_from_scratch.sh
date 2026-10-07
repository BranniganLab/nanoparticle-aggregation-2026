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

SECONDS=0
echo "Downloading data from zenodo..."
zenodo_get 18989520
zenodo_get 18991663
zenodo_get 22815650
zenodo_get 22813690

mkdir Multi_Nanoparticle
mkdir Multi_Nanoparticle/Dimer_Free_Energy_System

tar -xzvf Hydrophobic.tar.gz
tar -xzvf Polar.tar.gz
tar -xzvf 10_NP_Systems.tar.gz
tar -xzvf Single_Nanoparticle.tar.gz

mv 10_NP_Systems Multi_Nanoparticle/10_NP_Systems

rm Hydrophobic.tar.gz
rm Polar.tar.gz
rm 10_NP_Systems.tar.gz
rm Single_Nanoparticle.tar.gz

tar -xzvf Hydro_R2.tar.gz
tar -xzvf Hydro_R3.tar.gz
tar -xzvf Polar_R2.tar.gz
tar -xzvf Polar_R3.tar.gz

mv nas/Gold_Nanoparticle_Project/Martini_GNP_Paper/Simulation/Multi_Nanoparticle/Dimer_Free_Energy_System/Hydrophobic/Replica_2 Hydrophobic/
mv nas/Gold_Nanoparticle_Project/Martini_GNP_Paper/Simulation/Multi_Nanoparticle/Dimer_Free_Energy_System/Hydrophobic/Replica_3 Hydrophobic/
mv nas/Gold_Nanoparticle_Project/Martini_GNP_Paper/Simulation/Multi_Nanoparticle/Dimer_Free_Energy_System/Polar/Replica_2 Polar/
mv nas/Gold_Nanoparticle_Project/Martini_GNP_Paper/Simulation/Multi_Nanoparticle/Dimer_Free_Energy_System/Polar/Replica_3 Polar/
mv Polar Multi_Nanoparticle/Dimer_Free_Energy_System
mv Hydrophobic Multi_Nanoparticle/Dimer_Free_Energy_System
rm -rf nas
cp Multi_Nanoparticle/Dimer_Free_Energy_System/Hydrophobic/Replica_1/umbrella607* HMulti_Nanoparticle/Dimer_Free_Energy_System/Hydrophobic/Replica_2/
cp Multi_Nanoparticle/Dimer_Free_Energy_System/Polar/Replica_1/umbrella595* Multi_Nanoparticle/Dimer_Free_Energy_System/Polar/Replica_3/

rm Hydro_R2.tar.gz
rm Hydro_R3.tar.gz
rm Polar_R2.tar.gz
rm Polar_R3.tar.gz

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