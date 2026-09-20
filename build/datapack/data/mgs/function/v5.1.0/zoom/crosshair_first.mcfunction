
#> mgs:v5.1.0/zoom/crosshair_first
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zoom/crosshair_spread
#

# @s = a player who has no crosshair id yet, so the ramp starts and ends on the same level
data modify storage mgs:input crosshair set value {"from":0,"to":0}
execute store result storage mgs:input crosshair.to int 1 run scoreboard players get #spread mgs.data
data modify storage mgs:input crosshair.from set from storage mgs:input crosshair.to
function mgs:v5.1.0/zoom/crosshair_add with storage mgs:input crosshair
scoreboard players operation @s mgs.cross_from = #spread mgs.data
scoreboard players operation @s mgs.cross_to = #spread mgs.data

