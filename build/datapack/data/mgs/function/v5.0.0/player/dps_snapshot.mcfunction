
#> mgs:v5.0.0/player/dps_snapshot
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# Snapshot current DPS accumulator and reset for the next second
scoreboard players operation @s mgs.previous_dps = @s mgs.dps
scoreboard players set @s mgs.dps 0
scoreboard players set @s mgs.dps_timer 0

