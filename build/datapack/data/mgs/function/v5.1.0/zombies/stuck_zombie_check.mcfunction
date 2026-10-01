
#> mgs:v5.1.0/zombies/stuck_zombie_check
#
# @executed	as @e[tag=...,limit=24,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/game_tick [ as @e[tag=...,limit=24,sort=random] & at @s ]
#

# Run as a non-rising zombie_round, every 20 ticks on up to 24 random ones. Progress resets the timer.
# Timeout: 400 ticks without moving (100 once already rescued), 300 if it moves without getting closer.

# Distance bucket to the nearest alive player, 4 (very far) to 0 (adjacent).
scoreboard players set #cur_dist_bucket mgs.data 4
execute if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..96] run scoreboard players set #cur_dist_bucket mgs.data 3
execute if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..64] run scoreboard players set #cur_dist_bucket mgs.data 2
execute if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..32] run scoreboard players set #cur_dist_bucket mgs.data 1
execute if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..16] run scoreboard players set #cur_dist_bucket mgs.data 0

execute store result score #cur_x mgs.data run data get entity @s Pos[0]
execute store result score #cur_z mgs.data run data get entity @s Pos[2]

# Progress: the bucket improved, or bucket 0 with the player visible. Without the line-of-sight test a player
# above or below a floor kept the zombie "not stuck" forever. XZ movement is not progress: a zombie attacking stands still.
scoreboard players set #stuck_progress mgs.data 0
execute if score #cur_dist_bucket mgs.data < @s mgs.zb.stuck_dist run scoreboard players set #stuck_progress mgs.data 1
scoreboard players set #zb_stuck_see mgs.data 0
execute if score #cur_dist_bucket mgs.data matches 0 positioned as @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..16] store result score #zb_stuck_see mgs.data run function #bs.view:can_see_ata {with:{}}
execute if score #zb_stuck_see mgs.data matches 1 run scoreboard players set #stuck_progress mgs.data 1

# During a PaP-room lure, a zombie at the theatre centre is where it should be (see escort, lure mode).
execute if score #zb_lure mgs.data matches 1 if entity @e[tag=mgs.lure_center,distance=..12] run scoreboard players set #stuck_progress mgs.data 1

execute if score #stuck_progress mgs.data matches 1 run scoreboard players operation @s mgs.zb.stuck_dist = #cur_dist_bucket mgs.data
execute if score #stuck_progress mgs.data matches 1 run scoreboard players operation @s mgs.zb.stuck_x = #cur_x mgs.data
execute if score #stuck_progress mgs.data matches 1 run scoreboard players operation @s mgs.zb.stuck_z = #cur_z mgs.data
execute if score #stuck_progress mgs.data matches 1 run scoreboard players operation @s mgs.zb.stuck_ticks = #total_tick mgs.data
execute if score #stuck_progress mgs.data matches 1 run tag @s remove mgs.zb_rescued
execute if score #stuck_progress mgs.data matches 1 run return 0

# Moved: XZ differs from the snapshot at the last progress (block precision).
scoreboard players set #stuck_moved mgs.data 0
execute unless score #cur_x mgs.data = @s mgs.zb.stuck_x run scoreboard players set #stuck_moved mgs.data 1
execute unless score #cur_z mgs.data = @s mgs.zb.stuck_z run scoreboard players set #stuck_moved mgs.data 1
scoreboard players set #stuck_threshold mgs.data 400
execute if score #stuck_moved mgs.data matches 1 run scoreboard players set #stuck_threshold mgs.data 300
execute if score #stuck_moved mgs.data matches 0 if entity @s[tag=mgs.zb_rescued] run scoreboard players set #stuck_threshold mgs.data 100

# With 2 zombies left the timeout drops to 5 s, so a hard-to-reach zombie is rescued quickly.
execute if score #zb_alive mgs.data matches ..2 if score #stuck_threshold mgs.data matches 101.. run scoreboard players set #stuck_threshold mgs.data 100

scoreboard players operation #stuck_delta mgs.data = #total_tick mgs.data
scoreboard players operation #stuck_delta mgs.data -= @s mgs.zb.stuck_ticks
execute if score #stuck_delta mgs.data >= #stuck_threshold mgs.data run function mgs:v5.1.0/zombies/on_stuck_zombie

