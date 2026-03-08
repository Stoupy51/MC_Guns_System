
#> mgs:v5.0.0/zombies/perks/setup
#
# @within	mgs:v5.0.0/zombies/preload_complete
#

scoreboard players set #_pk_counter mgs.data 0
data modify storage mgs:zombies perk_data set value {}
data modify storage mgs:temp _pk_iter set from storage mgs:zombies game.map.perks
execute if data storage mgs:temp _pk_iter[0] run function mgs:v5.0.0/zombies/perks/setup_iter

