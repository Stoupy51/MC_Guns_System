
#> mgs:v5.0.0/zombies/doors/setup
#
# @within	mgs:v5.0.0/zombies/preload_complete
#

data modify storage mgs:temp _door_iter set from storage mgs:zombies game.map.doors
execute if data storage mgs:temp _door_iter[0] run function mgs:v5.0.0/zombies/doors/setup_iter

