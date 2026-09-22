
#> mgs:v5.1.0/zoom/crosshair_to_back
#
# @executed	at @s & anchored eyes & positioned ^ ^ ^0.001 & as @a[distance=..16]
#
# @within	mgs:v5.1.0/player/apply_flash_if_can_see
#			mgs:v5.1.0/player/apply_pap_flash_if_can_see
#

execute unless score @s mgs.cross_to matches -2147483648.. run return 0
data modify storage mgs:input crosshair set value {"from":0,"to":0}
execute store result storage mgs:input crosshair.from int 1 run scoreboard players get @s mgs.cross_from
execute store result storage mgs:input crosshair.to int 1 run scoreboard players get @s mgs.cross_to
function mgs:v5.1.0/zoom/crosshair_remove with storage mgs:input crosshair
function mgs:v5.1.0/zoom/crosshair_add with storage mgs:input crosshair

