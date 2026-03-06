
#> mgs:v5.0.0/missions/spawn_level
#
# @within	mgs:v5.0.0/missions/end_prep
#			mgs:v5.0.0/missions/level_cleared 60t [ scheduled ]
#

# Announce current level
execute if score #mi_level mgs.data matches 1 run tellraw @a ["",{"text":"","color":"green","bold":true},"  ▶ ",{"translate": "mgs.level_1"}]
execute if score #mi_level mgs.data matches 2 run tellraw @a ["",{"text":"","color":"yellow","bold":true},"  ▶ ",{"translate": "mgs.level_2"}]
execute if score #mi_level mgs.data matches 3 run tellraw @a ["",{"text":"","color":"gold","bold":true},"  ▶ ",{"translate": "mgs.level_3"}]
execute if score #mi_level mgs.data matches 4 run tellraw @a ["",{"text":"","color":"red","bold":true},"  ▶ ",{"translate": "mgs.level_4"}]

# Store base coordinates for offset
execute store result score #gm_base_x mgs.data run data get storage mgs:missions game.map.base_coordinates[0]
execute store result score #gm_base_y mgs.data run data get storage mgs:missions game.map.base_coordinates[1]
execute store result score #gm_base_z mgs.data run data get storage mgs:missions game.map.base_coordinates[2]

# Reset enemy count
scoreboard players set #mi_enemies mgs.data 0

# Dispatch to level-specific spawner
execute if score #mi_level mgs.data matches 1 run function mgs:v5.0.0/missions/spawn_level_1
execute if score #mi_level mgs.data matches 2 run function mgs:v5.0.0/missions/spawn_level_2
execute if score #mi_level mgs.data matches 3 run function mgs:v5.0.0/missions/spawn_level_3
execute if score #mi_level mgs.data matches 4 run function mgs:v5.0.0/missions/spawn_level_4

# Give a random gun to all enemies that don't have any gun
execute as @e[tag=mgs.mission_enemy] unless items entity @s weapon.mainhand * run function mgs:v5.0.0/utils/random_weapon {slot:"weapon.mainhand"}

