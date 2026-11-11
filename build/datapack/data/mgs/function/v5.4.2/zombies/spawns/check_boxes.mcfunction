
#> mgs:v5.4.2/zombies/spawns/check_boxes
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/game_tick
#

execute as @e[type=minecraft:marker,tag=mgs.spawn_has_abox,tag=mgs.spawn_unlocked] run function mgs:v5.4.2/zombies/spawns/check_box

