
#> mgs:v5.0.0/zombies/barriers/setup
#
# @within	mgs:v5.0.0/zombies/preload_complete
#

scoreboard players set #barrier_counter mgs.data 0
data modify storage mgs:temp _barrier_iter set from storage mgs:zombies game.map.barriers
execute if data storage mgs:temp _barrier_iter[0] run function mgs:v5.0.0/zombies/barriers/setup_iter

