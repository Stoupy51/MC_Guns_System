
#> mgs:v5.1.0/zoom/crosshair_swap
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zoom/crosshair_apply
#

# The applied id is crosshair_<cross_from>_<cross_to>, so the new ramp starts where that one ended
data modify storage mgs:input crosshair set value {"from":0,"to":0,"next":0}
execute store result storage mgs:input crosshair.from int 1 run scoreboard players get @s mgs.cross_from
execute store result storage mgs:input crosshair.to int 1 run scoreboard players get @s mgs.cross_to
execute store result storage mgs:input crosshair.next int 1 run scoreboard players get #spread mgs.data
function mgs:v5.1.0/zoom/crosshair_replace with storage mgs:input crosshair
scoreboard players operation @s mgs.cross_from = @s mgs.cross_to
scoreboard players operation @s mgs.cross_to = #spread mgs.data

