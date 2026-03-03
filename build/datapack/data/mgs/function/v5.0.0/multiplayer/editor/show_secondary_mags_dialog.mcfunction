
#> mgs:v5.0.0/multiplayer/editor/show_secondary_mags_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/pick_secondary
#			mgs:v5.0.0/multiplayer/editor/pick_secondary_scope
#

execute store result storage mgs:temp _pts int 1 run scoreboard players get @s mgs.mp.edit_points
function mgs:v5.0.0/multiplayer/editor/show_secondary_mags_dialog_macro with storage mgs:temp

