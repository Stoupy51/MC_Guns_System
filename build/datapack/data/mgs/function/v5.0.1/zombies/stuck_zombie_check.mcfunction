
#> mgs:v5.0.1/zombies/stuck_zombie_check
#
# @executed	as @e[tag=...,limit=24,sort=random] & at @s
#
# @within	mgs:v5.0.1/zombies/game_tick [ as @e[tag=...,limit=24,sort=random] & at @s ]
#

# @s = zombie_round entity (non-rising), run every 20 ticks on up to 24 random zombies
# Progress = distance bucket improved (or a player in melee range is VISIBLE). Resets the timer.
# Timeout depends on HOW the zombie is stuck:
# - hasn't moved at all: 400t (20s), only 100t (5s) once it has already been rescued
# - moved since last progress but not getting closer to a player: 300t (15s)

# Compute distance bucket to nearest alive player (4=very far, 0=adjacent)
scoreboard players set #cur_dist_bucket mgs.data 4
execute if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..96] run scoreboard players set #cur_dist_bucket mgs.data 3
execute if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..64] run scoreboard players set #cur_dist_bucket mgs.data 2
execute if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..32] run scoreboard players set #cur_dist_bucket mgs.data 1
execute if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..16] run scoreboard players set #cur_dist_bucket mgs.data 0

# Compute current XZ position
execute store result score #cur_x mgs.data run data get entity @s Pos[0]
execute store result score #cur_z mgs.data run data get entity @s Pos[2]

# Detect any progress: bucket improved, OR bucket == 0 AND the nearby player is actually
# VISIBLE (real melee range). Proximity alone is not enough: a player a few blocks above or
# below through a floor kept the zombie permanently "not stuck" while it could never reach
# them — the LOS gate lets the timer run so the escort picks it up (see escort.py).
# XZ movement is NOT checked: a zombie attacking at close range stands still legitimately
scoreboard players set #stuck_progress mgs.data 0
execute if score #cur_dist_bucket mgs.data < @s mgs.zb.stuck_dist run scoreboard players set #stuck_progress mgs.data 1
scoreboard players set #zb_stuck_see mgs.data 0
execute if score #cur_dist_bucket mgs.data matches 0 positioned as @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..16] store result score #zb_stuck_see mgs.data run function #bs.view:can_see_ata {with:{}}
execute if score #zb_stuck_see mgs.data matches 1 run scoreboard players set #stuck_progress mgs.data 1

# If progress: update all stored values, reset timestamp, and clear the rescued flag
execute if score #stuck_progress mgs.data matches 1 run scoreboard players operation @s mgs.zb.stuck_dist = #cur_dist_bucket mgs.data
execute if score #stuck_progress mgs.data matches 1 run scoreboard players operation @s mgs.zb.stuck_x = #cur_x mgs.data
execute if score #stuck_progress mgs.data matches 1 run scoreboard players operation @s mgs.zb.stuck_z = #cur_z mgs.data
execute if score #stuck_progress mgs.data matches 1 run scoreboard players operation @s mgs.zb.stuck_ticks = #total_tick mgs.data
execute if score #stuck_progress mgs.data matches 1 run tag @s remove mgs.zb_rescued
execute if score #stuck_progress mgs.data matches 1 run return 0

# No progress: pick the timeout for this stuck mode
# Moved = XZ differs from the snapshot taken at the last progress (block precision)
scoreboard players set #stuck_moved mgs.data 0
execute unless score #cur_x mgs.data = @s mgs.zb.stuck_x run scoreboard players set #stuck_moved mgs.data 1
execute unless score #cur_z mgs.data = @s mgs.zb.stuck_z run scoreboard players set #stuck_moved mgs.data 1
scoreboard players set #stuck_threshold mgs.data 400
execute if score #stuck_moved mgs.data matches 1 run scoreboard players set #stuck_threshold mgs.data 300
execute if score #stuck_moved mgs.data matches 0 if entity @s[tag=mgs.zb_rescued] run scoreboard players set #stuck_threshold mgs.data 100

# Compute elapsed ticks since last progress; respawn once the timeout is reached
scoreboard players operation #stuck_delta mgs.data = #total_tick mgs.data
scoreboard players operation #stuck_delta mgs.data -= @s mgs.zb.stuck_ticks
execute if score #stuck_delta mgs.data >= #stuck_threshold mgs.data run function mgs:v5.0.1/zombies/on_stuck_zombie

