puts "Processing File"
set empath [lindex $argv 0]
mol new $empath waitfor all
mol addfile md_reduced.xtc waitfor all
source ../../../../../Figure_3/cluster.tcl
ClusterControl AU 10 2 0 -1 "analysis/fullcluster"
puts "Finished Processing"
