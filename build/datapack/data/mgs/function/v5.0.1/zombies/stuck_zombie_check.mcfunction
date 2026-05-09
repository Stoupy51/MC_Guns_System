
#> mgs:v5.0.1/zombies/stuck_zombie_check
#
# @executed	as @e[tag=...,limit=24,sort=random]
#
# @within	mgs:v5.0.1/zombies/game_tick [ as @e[tag=...,limit=24,sort=random] ]
#

# @s = zombie_round entity (non-rising), run every 20 ticks on up to 24 random zombies
execute store result score #cur_x mgs.data run data get entity @s Pos[0]
execute store result score #cur_z mgs.data run data get entity @s Pos[2]

# Check if zombie moved on X or Z
scoreboard players set #stuck_moved mgs.data 0
execute unless score #cur_x mgs.data = @s mgs.zb.stuck_x run scoreboard players set #stuck_moved mgs.data 1
execute unless score #cur_z mgs.data = @s mgs.zb.stuck_z run scoreboard players set #stuck_moved mgs.data 1

# If moved: update stored position and timestamp
execute if score #stuck_moved mgs.data matches 1 run scoreboard players operation @s mgs.zb.stuck_x = #cur_x mgs.data
execute if score #stuck_moved mgs.data matches 1 run scoreboard players operation @s mgs.zb.stuck_z = #cur_z mgs.data
execute if score #stuck_moved mgs.data matches 1 run scoreboard players operation @s mgs.zb.stuck_ticks = #total_tick mgs.data

# If still: compute delta ticks and kill if >= 300 (15s)
execute if score #stuck_moved mgs.data matches 0 run scoreboard players operation #stuck_delta mgs.data = #total_tick mgs.data
execute if score #stuck_moved mgs.data matches 0 run scoreboard players operation #stuck_delta mgs.data -= @s mgs.zb.stuck_ticks
execute if score #stuck_moved mgs.data matches 0 if score #stuck_delta mgs.data matches 300.. run function mgs:v5.0.1/zombies/on_stuck_zombie

