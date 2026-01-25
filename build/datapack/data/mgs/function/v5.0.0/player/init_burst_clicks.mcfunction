
#> mgs:v5.0.0/player/init_burst_clicks
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/right_click
#

# Calculate (BURST - 1) * COOLDOWN
execute store result score #burst_clicks mgs.data run data get storage mgs:gun all.stats.burst
scoreboard players remove #burst_clicks mgs.data 1
execute store result score #cooldown_value mgs.data run data get storage mgs:gun all.stats.cooldown
scoreboard players operation #burst_clicks mgs.data *= #cooldown_value mgs.data

# Set pending_clicks to sustain burst firing
scoreboard players operation @s mgs.pending_clicks = #burst_clicks mgs.data

