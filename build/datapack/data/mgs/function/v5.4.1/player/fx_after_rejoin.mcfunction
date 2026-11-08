
#> mgs:v5.4.1/player/fx_after_rejoin
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.4.1/player/tick
#			mgs:v5.4.1/dialog/close_then
#

function mgs:v5.4.1/player/fx_reset
scoreboard players set @s mgs.fx_rejoins 0

