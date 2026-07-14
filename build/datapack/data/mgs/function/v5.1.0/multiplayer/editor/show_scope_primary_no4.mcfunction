
#> mgs:v5.1.0/multiplayer/editor/show_scope_primary_no4
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/editor/scope/primary_no4
#

function mgs:v5.1.0/multiplayer/editor/recompute_points
execute store result storage mgs:temp _pts int 1 run scoreboard players get @s mgs.mp.edit_points
function mgs:v5.1.0/multiplayer/editor/show_scope_primary_no4_macro with storage mgs:temp

