
#> mgs:v5.0.1/maps/zombies/kino_der_toten/register
#
# @within	#mgs:zombies/register_maps
#

# Kino der Toten map registration
execute unless data storage mgs:maps zombies[{id:"kino_der_toten"}] run data modify storage mgs:maps zombies append value {id:"kino_der_toten", name:"Kino der Toten", description:"Black Ops 1 | Classic Zombies", base_coordinates:[0,0,0], spawning_points:{zombies:[],players:[]}, out_of_bounds:[], boundaries:[]}

