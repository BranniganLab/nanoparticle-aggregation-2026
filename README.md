# Martini_GNP_Paper
Repository for storing scripts, data, and simulation set-up associated with the Martini Gold Nanoparticle paper. 
Simulations are stored on Amarel(/projects/ccib/brannigan/jje63/Gold_Nanoparticle_Project/) and [this Zenodo](https://doi.org/10.5281/zenodo.18989519) and [this Zenodo](https://doi.org/10.5281/zenodo.18991662). Simulations are not necessary to run any of the analysis scripts, as all data from the simulations associated with the paper is stored in the Simulation folder.

To make the figures from *Assessing the Aggregation Behavior of Coarse-Grained Martini Nanoparticle Models in Lipid Environments paper* do the following:

1. Clone this repository. You do not need the accompanying zenodo to remake the figures. All calculated values from trajectories have been written to files.
2. cd into repository and Create a virtual environment:
    - Conda: `conda env create -f environment.yml` -> `conda activate gnppaper`
    - python: `python -m venv gnppaper` -> `source gnppaper/bin/activate`
3. cd into the **Figure_Making_Scripts** folder
4. Make the figures:
    - To remake all figures run the command: `bash make_all_figures.sh`
    - To remake a specific figure run the command: `python [name of figure] [optional showplot -sp]` Example: `python Figure1.py -sp`

