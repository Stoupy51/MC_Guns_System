
#> mgs:v5.0.0/multiplayer/gamemodes/hp/tick
#
# @within	mgs:v5.0.0/multiplayer/game_tick
#

# Rotation timer
scoreboard players remove #hp_rotate_timer mgs.data 1
execute if score #hp_rotate_timer mgs.data matches ..0 run function mgs:v5.0.0/multiplayer/gamemodes/hp/rotate

# Update seconds display for sidebar (ticks / 20)
scoreboard players operation #hp_rotate_sec mgs.data = #hp_rotate_timer mgs.data
scoreboard players operation #hp_rotate_sec mgs.data /= #20 mgs.data

# Refresh sidebar every second (when score_timer resets)
execute if score #hp_score_timer mgs.data matches ..1 run function #bs.sidebar:refresh {objective:"mgs.sidebar"}

# Show particles at zone center
execute at @e[tag=mgs.hp_marker] run particle dust{color:[0.5,0.0,0.5],scale:1.5} ~ ~ ~ 4 0.5 4 0 10

# Tag players inside the zone (within 5 blocks horizontally, 4 blocks vertically)
tag @a remove mgs.in_hp_zone
execute at @e[tag=mgs.hp_marker] positioned ~-2 ~ ~-2 run tag @a[dx=5,dy=5,dz=5] add mgs.in_hp_zone

# Count teams in zone
execute store result score #hp_red mgs.data if entity @a[tag=mgs.in_hp_zone,scores={mgs.mp.team=1}]
execute store result score #hp_blue mgs.data if entity @a[tag=mgs.in_hp_zone,scores={mgs.mp.team=2}]

# Scoring interval
scoreboard players remove #hp_score_timer mgs.data 1
execute if score #hp_score_timer mgs.data matches ..0 run function mgs:v5.0.0/multiplayer/gamemodes/hp/score_tick
execute if score #hp_score_timer mgs.data matches ..0 run scoreboard players set #hp_score_timer mgs.data 20

