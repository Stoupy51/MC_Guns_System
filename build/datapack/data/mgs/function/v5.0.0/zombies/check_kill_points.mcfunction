
#> mgs:v5.0.0/zombies/check_kill_points
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.0.0/zombies/game_tick [ as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] ]
#

# Calculate delta kills since last check
scoreboard players operation #zb_kills_delta mgs.data = @s mgs.total_kills
scoreboard players operation #zb_kills_delta mgs.data -= @s mgs.zb.prev_kills
scoreboard players operation @s mgs.zb.prev_kills = @s mgs.total_kills

# Skip if no new kills
execute if score #zb_kills_delta mgs.data matches ..0 run return 0

# Determine kill type: gun (bullet kill = 50) or melee (knife kill = 130)
scoreboard players set #zb_kill_points mgs.data 0
execute if items entity @s weapon.mainhand *[custom_data~{mgs:{gun:true}}] run scoreboard players operation #zb_kill_points mgs.data = #zb_points_kill mgs.config
execute unless items entity @s weapon.mainhand *[custom_data~{mgs:{gun:true}}] run scoreboard players operation #zb_kill_points mgs.data = #zb_points_knife_kill mgs.config

# Award base points (delta * points_per_kill_type)
scoreboard players operation #total_kill_points mgs.data = #zb_kills_delta mgs.data
scoreboard players operation #total_kill_points mgs.data *= #zb_kill_points mgs.data
scoreboard players operation @s mgs.zb.points += #total_kill_points mgs.data

# Apply x1.2 points passive: add 20% extra
execute if score @s mgs.zb.passive matches 1 run scoreboard players operation #additional mgs.data = #total_kill_points mgs.data
execute if score @s mgs.zb.passive matches 1 run scoreboard players operation #additional mgs.data /= #5 mgs.data
execute if score @s mgs.zb.passive matches 1 run scoreboard players operation @s mgs.zb.points += #additional mgs.data

# Accumulate kill count
scoreboard players operation @s mgs.zb.kills += #zb_kills_delta mgs.data

