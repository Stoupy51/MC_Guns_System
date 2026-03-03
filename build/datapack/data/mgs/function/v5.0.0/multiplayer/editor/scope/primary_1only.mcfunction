
#> mgs:v5.0.0/multiplayer/editor/scope/primary_1only
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/pick_primary
#

execute store result storage mgs:temp _pts int 1 run scoreboard players get @s mgs.mp.edit_points
function mgs:v5.0.0/multiplayer/editor/scope/primary_1only_macro with storage mgs:temp

