
#> mgs:v5.0.1/multiplayer/editor/show_secondary_pistol_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/multiplayer/editor/show_secondary_dialog
#

function mgs:v5.0.1/multiplayer/editor/recompute_points
execute store result storage mgs:temp _pts int 1 run scoreboard players get @s mgs.mp.edit_points
function mgs:v5.0.1/multiplayer/editor/show_secondary_pistol_dialog_macro with storage mgs:temp

