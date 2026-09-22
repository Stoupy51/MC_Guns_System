
#> mgs:v5.1.0/zoom/crosshair_clear
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zoom/main
#

# @s = a player who is aiming down sights or no longer holding a gun
execute unless score @s mgs.cross_to matches -2147483648.. run return 0
data modify storage mgs:input crosshair set value {"from":0,"to":0}
execute store result storage mgs:input crosshair.from int 1 run scoreboard players get @s mgs.cross_from
execute store result storage mgs:input crosshair.to int 1 run scoreboard players get @s mgs.cross_to
function mgs:v5.1.0/zoom/crosshair_remove with storage mgs:input crosshair
scoreboard players reset @s mgs.cross_from
scoreboard players reset @s mgs.cross_to

