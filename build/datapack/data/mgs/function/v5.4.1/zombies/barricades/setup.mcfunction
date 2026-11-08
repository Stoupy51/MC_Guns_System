
#> mgs:v5.4.1/zombies/barricades/setup
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/preload_complete
#

scoreboard players set #barricade_counter mgs.data 0
data modify storage mgs:temp _barricade_iter set from storage mgs:zombies game.map.barricades
execute if data storage mgs:temp _barricade_iter[0] run function mgs:v5.4.1/zombies/barricades/setup_iter

