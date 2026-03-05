
#> mgs:v5.0.0/multiplayer/gamemodes/hp/tick
#
# @within	mgs:v5.0.0/multiplayer/game_tick
#

# Rotation timer
scoreboard players remove #hp_rotate_timer mgs.data 1
execute if score #hp_rotate_timer mgs.data matches ..0 run function mgs:v5.0.0/multiplayer/gamemodes/hp/rotate

# Show particles at zone corners
execute at @e[tag=mgs.hp_corner] run particle dust{color:[0.5,0.0,0.5],scale:1.5} ~ ~1 ~ 4 0.5 4 0 10

# Count teams in zone: check players between the two corners
# Store corner A position
execute as @e[tag=mgs.hp_corner_a] store result score #hp_ax mgs.data run data get entity @s Pos[0]
execute as @e[tag=mgs.hp_corner_a] store result score #hp_ay mgs.data run data get entity @s Pos[1]
execute as @e[tag=mgs.hp_corner_a] store result score #hp_az mgs.data run data get entity @s Pos[2]
# Store corner B position
execute as @e[tag=mgs.hp_corner_b] store result score #hp_bx mgs.data run data get entity @s Pos[0]
execute as @e[tag=mgs.hp_corner_b] store result score #hp_by mgs.data run data get entity @s Pos[1]
execute as @e[tag=mgs.hp_corner_b] store result score #hp_bz mgs.data run data get entity @s Pos[2]

# Tag players inside the zone (between both corners with 3-block margin)
# Using positioned checking: player must be within 8 blocks of BOTH corners
tag @a remove mgs.in_hp_zone
execute at @e[tag=mgs.hp_corner_a] as @a[distance=..15] at @s at @e[tag=mgs.hp_corner_b,distance=..15] run tag @s add mgs.in_hp_zone

# Count teams in zone
execute store result score #hp_red mgs.data if entity @a[tag=mgs.in_hp_zone,scores={mgs.mp.team=1}]
execute store result score #hp_blue mgs.data if entity @a[tag=mgs.in_hp_zone,scores={mgs.mp.team=2}]

# Scoring interval
scoreboard players remove #hp_score_timer mgs.data 1
execute if score #hp_score_timer mgs.data matches ..0 run function mgs:v5.0.0/multiplayer/gamemodes/hp/score_tick
execute if score #hp_score_timer mgs.data matches ..0 run scoreboard players set #hp_score_timer mgs.data 20

