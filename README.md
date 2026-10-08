# Martini_GNP_Paper
Repository for storing scripts, data, and simulation set-up associated with the Martini Gold Nanoparticle paper. 
Simulations are stored on Amarel(/projects/ccib/brannigan/jje63/Gold_Nanoparticle_Project/) and on Zenodo: [Zenodo 1](https://doi.org/10.5281/zenodo.18989519), [Zenodo 2](https://doi.org/10.5281/zenodo.18991662), [Zenodo 3](https://zenodo.org/records/22813690), [Zenodo 4](https://zenodo.org/records/22815650). Simulations are not necessary to run any of the analysis scripts, as all data from the simulations associated with the paper is stored in the Simulation folder. However, if you wish to recreate the data from the simulation, this can be done with the scripts in the Zenodo folder.

## Recreating Figures from Precomputed Outputs
To make the figures from [*The Core Matters: Aggregation of Neutral Ligand-Coated Nanoparticles in Membranes*](https://pubs.acs.org/jpcbfk/article/130/37/9496/5394074/The-Core-Matters-Aggregation-of-Neutral-Ligand) do the following:

1. Clone this repository. You do not need the accompanying zenodo to remake the figures. All calculated values from trajectories have been written to files.
2. cd into repository and create a virtual environment:
    - Conda:
      1. `conda env create -f environment.yml;conda activate gnppaper`
    - Python:
      1. `python -m venv gnppaper;source gnppaper/bin/activate`\
      2. `pip install -r requirements.txt` 
3. cd into the **Figure_Making_Scripts** folder
4. Make the figures:
    - To remake all figures run the command: `bash make_all_figures.sh`
    - To remake a specific figure run the command: `python [name of figure] [optional showplot -sp]` Example: `python Figure1.py -sp`
5. Figures will show up in the **Graphs** folder

## Making figures from Simulation Data (.xtc and .gro files)
Recreating figures from simulation data will take roughly 7-18 hours depending on zenodo download speeds. However, the process can be done and has been fully automated using the bash scripts in the zenodo folder. One note is that Gromacs and VMD are required in order to recreate the figures from simulation data as a Gromacs rerun is performed on the .xtc files in order to generate the force and position data used in recreating the free energy profiles with GMX WHAM. 

1. Follow steps 1 and 2 from above.
2. cd into the **Zenodo** folder
3. run the command `bash create_data_from_scratch.sh`
