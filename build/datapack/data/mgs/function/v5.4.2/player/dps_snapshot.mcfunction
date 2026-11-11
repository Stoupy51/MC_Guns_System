
#> mgs:v5.4.2/player/dps_snapshot
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.4.2/player/tick
#			mgs:v5.4.2/dialog/close_then
#

scoreboard players operation @s mgs.previous_dps = @s mgs.dps
scoreboard players set @s mgs.dps 0
scoreboard players set @s mgs.dps_timer 0

