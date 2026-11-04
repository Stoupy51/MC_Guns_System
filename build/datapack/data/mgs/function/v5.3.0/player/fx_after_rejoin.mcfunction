
#> mgs:v5.3.0/player/fx_after_rejoin
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/player/tick
#			mgs:v5.3.0/dialog/close_then
#

function mgs:v5.3.0/player/fx_reset
scoreboard players set @s mgs.fx_rejoins 0

