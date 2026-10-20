
#> mgs:v5.2.0/player/burst_cooldown
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.2.0/player/right_click
#

execute if data storage mgs:gun all.stats.fire_modes[0].burst_spacing store result score #cooldown mgs.data run data get storage mgs:gun all.stats.fire_modes[0].burst_spacing

# First round: pending_clicks = (burst - 1) x spacing sustains the burst without the button held.
execute if score @s mgs.burst_count matches 0 run scoreboard players operation @s mgs.pending_clicks = #burst_limit mgs.data
execute if score @s mgs.burst_count matches 0 run scoreboard players remove @s mgs.pending_clicks 1
execute if score @s mgs.burst_count matches 0 run scoreboard players operation @s mgs.pending_clicks *= #cooldown mgs.data

scoreboard players add @s mgs.burst_count 1

# Last round: the pause before the next burst.
scoreboard players set #burst_pause mgs.data 0
execute if score @s mgs.burst_count >= #burst_limit mgs.data store result score #burst_pause mgs.data run data get storage mgs:gun all.stats.fire_modes[0].burst_pause
scoreboard players operation #cooldown mgs.data += #burst_pause mgs.data

