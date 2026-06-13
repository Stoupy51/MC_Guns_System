
#> mgs:v5.0.1/multiplayer/editor/show_scope_primary_1only
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/multiplayer/editor/scope/primary_1only
#

function mgs:v5.0.1/multiplayer/editor/recompute_points
execute store result storage mgs:temp _pts int 1 run scoreboard players get @s mgs.mp.edit_points
function mgs:v5.0.1/multiplayer/editor/show_scope_primary_1only_macro with storage mgs:temp

