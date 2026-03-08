
#> mgs:v5.0.0/zombies/traps/setup
#
# @within	mgs:v5.0.0/zombies/preload_complete
#

scoreboard players set #_trap_counter mgs.data 0
data modify storage mgs:temp _trap_iter set from storage mgs:zombies game.map.traps
execute if data storage mgs:temp _trap_iter[0] run function mgs:v5.0.0/zombies/traps/setup_iter

