
#> mgs:v5.0.0/multiplayer/editor/show_equip_slot1_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/pick_secondary
#			mgs:v5.0.0/multiplayer/editor/pick_secondary_mags
#			mgs:v5.0.0/multiplayer/editor/back_to_equip1
#

scoreboard players set @s mgs.mp.edit_step 3
execute store result storage mgs:temp _pts int 1 run scoreboard players get @s mgs.mp.edit_points
function mgs:v5.0.0/multiplayer/editor/show_equip_slot1_dialog_macro with storage mgs:temp

