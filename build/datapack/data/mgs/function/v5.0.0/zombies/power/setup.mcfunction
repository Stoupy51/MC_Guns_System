
#> mgs:v5.0.0/zombies/power/setup
#
# @within	mgs:v5.0.0/zombies/preload_complete
#

# Iterate power switch compounds from map data
data modify storage mgs:temp _pw_iter set from storage mgs:zombies game.map.power_switch
execute if data storage mgs:temp _pw_iter[0] run function mgs:v5.0.0/zombies/power/setup_iter

