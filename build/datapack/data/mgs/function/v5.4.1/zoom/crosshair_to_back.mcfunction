
#> mgs:v5.4.1/zoom/crosshair_to_back
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/player/apply_flash
#			mgs:v5.4.1/player/apply_pap_flash
#

execute unless score @s mgs.cross_to matches -2147483648.. run return 0
data modify storage mgs:input crosshair set value {"from":0,"to":0}
execute store result storage mgs:input crosshair.from int 1 run scoreboard players get @s mgs.cross_from
execute store result storage mgs:input crosshair.to int 1 run scoreboard players get @s mgs.cross_to
function mgs:v5.4.1/zoom/crosshair_remove with storage mgs:input crosshair
function mgs:v5.4.1/zoom/crosshair_add with storage mgs:input crosshair

