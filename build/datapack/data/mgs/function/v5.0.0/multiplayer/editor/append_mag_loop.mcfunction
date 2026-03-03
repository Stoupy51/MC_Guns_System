
#> mgs:v5.0.0/multiplayer/editor/append_mag_loop
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/append_mag_slots
#			mgs:v5.0.0/multiplayer/editor/append_mag_loop
#

execute if score #pmag_count mgs.data matches ..0 run return 0
execute store result storage mgs:temp _inv_n int 1 run scoreboard players get #inv_slot mgs.data
function mgs:v5.0.0/multiplayer/editor/append_mag_regular with storage mgs:temp
scoreboard players add #inv_slot mgs.data 1
scoreboard players remove #pmag_count mgs.data 1
return run function mgs:v5.0.0/multiplayer/editor/append_mag_loop

