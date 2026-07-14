
#> mgs:v5.1.0/multiplayer/editor/show_scope_secondary_4only
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/editor/scope/secondary_4only
#

function mgs:v5.1.0/multiplayer/editor/recompute_points
execute store result storage mgs:temp _pts int 1 run scoreboard players get @s mgs.mp.edit_points
function mgs:v5.1.0/multiplayer/editor/show_scope_secondary_4only_macro with storage mgs:temp

