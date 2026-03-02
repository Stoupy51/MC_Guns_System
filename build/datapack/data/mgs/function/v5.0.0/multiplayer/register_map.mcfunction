
#> mgs:v5.0.0/multiplayer/register_map
#
# @within	???
#

# Append map from mgs:input multiplayer.map to the maps list
# Expected format: {name:"map_name", spawns:{red:[x,y,z], blue:[x,y,z]}, flags:{red:[x,y,z], blue:[x,y,z]}}
data modify storage mgs:multiplayer maps append from storage mgs:input multiplayer.map

