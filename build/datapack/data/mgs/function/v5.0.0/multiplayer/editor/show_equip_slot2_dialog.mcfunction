
#> mgs:v5.0.0/multiplayer/editor/show_equip_slot2_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/pick_equip_slot1
#			mgs:v5.0.0/multiplayer/editor/back_from_perks
#

execute store result storage mgs:temp _pts int 1 run scoreboard players get @s mgs.mp.edit_points
function mgs:v5.0.0/multiplayer/editor/show_equip_slot2_dialog_macro with storage mgs:temp

