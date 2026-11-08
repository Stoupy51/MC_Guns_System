
#> mgs:v5.4.1/player/dps_snapshot
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.4.1/player/tick
#			mgs:v5.4.1/dialog/close_then
#

scoreboard players operation @s mgs.previous_dps = @s mgs.dps
scoreboard players set @s mgs.dps 0
scoreboard players set @s mgs.dps_timer 0

