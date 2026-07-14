
#> mgs:v5.1.0/multiplayer/editor/show_primary_mags_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process
#

execute if data storage mgs:temp editor{primary:""} run return run function mgs:v5.1.0/multiplayer/editor/hub
function mgs:v5.1.0/multiplayer/editor/recompute_points
execute store result storage mgs:temp _pts int 1 run scoreboard players get @s mgs.mp.edit_points
function mgs:v5.1.0/multiplayer/editor/show_primary_mags_dialog_macro with storage mgs:temp

