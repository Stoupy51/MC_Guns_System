
#> mgs:v5.0.0/player/check_mid_burst
#
# @executed	as the player & at current position
#
# @within	mgs:v5.0.0/player/set_pending_clicks
#

# Get burst limit
execute store result score #burst_limit mgs.data run data get storage mgs:gun all.stats.burst

# If burst_count < burst_limit, we're mid-burst
execute if score @s mgs.burst_count < #burst_limit mgs.data run scoreboard players set #is_mid_burst mgs.data 1

