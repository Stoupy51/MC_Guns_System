
#> mgs:v5.0.1/zombies/stuck_zombie_check
#
# @executed	as @e[tag=...,limit=24,sort=random] & at @s
#
# @within	mgs:v5.0.1/zombies/game_tick [ as @e[tag=...,limit=24,sort=random] & at @s ]
#

# @s = zombie_round entity (non-rising), run every 20 ticks on up to 24 random zombies
# Progress = distance bucket improved OR XZ position changed. Either resets the timer.

# Compute distance bucket to nearest alive player (4=very far, 0=adjacent)
scoreboard players set #cur_dist_bucket mgs.data 4
execute if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..96] run scoreboard players set #cur_dist_bucket mgs.data 3
execute if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..64] run scoreboard players set #cur_dist_bucket mgs.data 2
execute if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..32] run scoreboard players set #cur_dist_bucket mgs.data 1
execute if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..16] run scoreboard players set #cur_dist_bucket mgs.data 0

# Compute current XZ position
execute store result score #cur_x mgs.data run data get entity @s Pos[0]
execute store result score #cur_z mgs.data run data get entity @s Pos[2]

# Detect any progress: bucket improved, OR bucket == 0 (zombie is in melee range — not stuck)
# XZ movement is NOT checked: a zombie attacking at close range stands still legitimately
scoreboard players set #stuck_progress mgs.data 0
execute if score #cur_dist_bucket mgs.data < @s mgs.zb.stuck_dist run scoreboard players set #stuck_progress mgs.data 1
execute if score #cur_dist_bucket mgs.data matches 0 run scoreboard players set #stuck_progress mgs.data 1

# If progress: update all stored values and reset timestamp
execute if score #stuck_progress mgs.data matches 1 run scoreboard players operation @s mgs.zb.stuck_dist = #cur_dist_bucket mgs.data
execute if score #stuck_progress mgs.data matches 1 run scoreboard players operation @s mgs.zb.stuck_x = #cur_x mgs.data
execute if score #stuck_progress mgs.data matches 1 run scoreboard players operation @s mgs.zb.stuck_z = #cur_z mgs.data
execute if score #stuck_progress mgs.data matches 1 run scoreboard players operation @s mgs.zb.stuck_ticks = #total_tick mgs.data

# If no progress: compute elapsed ticks; respawn if >= 300 (15s)
execute if score #stuck_progress mgs.data matches 0 run scoreboard players operation #stuck_delta mgs.data = #total_tick mgs.data
execute if score #stuck_progress mgs.data matches 0 run scoreboard players operation #stuck_delta mgs.data -= @s mgs.zb.stuck_ticks
execute if score #stuck_progress mgs.data matches 0 if score #stuck_delta mgs.data matches 300.. run function mgs:v5.0.1/zombies/on_stuck_zombie

