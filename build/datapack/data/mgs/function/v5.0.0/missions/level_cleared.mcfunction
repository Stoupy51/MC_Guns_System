
#> mgs:v5.0.0/missions/level_cleared
#
# @within	mgs:v5.0.0/missions/game_tick
#

# Check if all 4 levels are done
execute if score #mi_level mgs.data matches 4 run return run function mgs:v5.0.0/missions/victory

# Announce
execute if score #mi_level mgs.data matches 1 run tellraw @a ["",{"text":"","color":"green","bold":true},"  ✔ ",{"translate": "mgs.level_1_cleared"}]
execute if score #mi_level mgs.data matches 2 run tellraw @a ["",{"text":"","color":"yellow","bold":true},"  ✔ ",{"translate": "mgs.level_2_cleared"}]
execute if score #mi_level mgs.data matches 3 run tellraw @a ["",{"text":"","color":"gold","bold":true},"  ✔ ",{"translate": "mgs.level_3_cleared"}]

# Advance to next level after short delay (3 seconds)
scoreboard players add #mi_level mgs.data 1
schedule function mgs:v5.0.0/missions/spawn_level 60t

