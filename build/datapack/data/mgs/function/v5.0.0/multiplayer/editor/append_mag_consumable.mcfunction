
#> mgs:v5.0.0/multiplayer/editor/append_mag_consumable
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/append_mag_slots
#

execute store result storage mgs:temp _inv_n int 1 run scoreboard players get #inv_slot mgs.data
function mgs:v5.0.0/multiplayer/editor/append_mag_consumable_macro with storage mgs:temp
scoreboard players add #inv_slot mgs.data 1

