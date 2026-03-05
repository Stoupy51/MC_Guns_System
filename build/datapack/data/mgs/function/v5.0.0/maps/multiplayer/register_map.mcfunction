
#> mgs:v5.0.0/maps/multiplayer/register_map
#
# @within	???
#

# Append map from mgs:input multiplayer.map to the maps list
# Expected format: {id:"id", name:"Name", description:"Desc", base_coordinates:[x,y,z],
#   boundaries:[], spawning_points:{red:[], blue:[], general:[]},
#   out_of_bounds:[], search_and_destroy:[], domination:[], hardpoint:[],
#   start_script:"...", tick_script:"...", join_script:"...", leave_script:"...", respawn_script:"..."}
data modify storage mgs:maps multiplayer append from storage mgs:input multiplayer.map

