
#> mgs:v5.0.0/player/reset_burst_if_complete
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# Check if in burst mode
execute store result score #fire_mode_is_burst mgs.data if data storage mgs:gun all.stats{fire_mode:"burst"}

# If not in burst mode, always reset
execute if score #fire_mode_is_burst mgs.data matches 0 run scoreboard players set @s mgs.burst_count 0
execute if score #fire_mode_is_burst mgs.data matches 0 run return 0

# If in burst mode, only reset if burst completed
execute store result score #burst_limit mgs.data run data get storage mgs:gun all.stats.burst
execute if score @s mgs.burst_count >= #burst_limit mgs.data run scoreboard players set @s mgs.burst_count 0

