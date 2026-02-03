puts "Processing File"
mol new em.gro waitfor all
mol addfile md_reduced.xtc waitfor all
source ~/Documents/Github_Repos/Martini_GNP_Paper/Analysis/Figure_3_scripts/cluster.tcl
ClusterControl AU 10 2 0 -1 "fullcluster"
puts "Finished Processing"