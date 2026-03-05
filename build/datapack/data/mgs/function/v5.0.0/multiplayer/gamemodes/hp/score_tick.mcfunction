
#> mgs:v5.0.0/multiplayer/gamemodes/hp/score_tick
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/hp/tick
#

# Only score if one team exclusively holds the zone (not contested)
# Red alone in zone
execute if score #hp_red mgs.data matches 1.. unless score #hp_blue mgs.data matches 1.. at @e[tag=mgs.hp_corner] run playsound minecraft:block.note_block.bell player @a ~ ~ ~ 1 1.2
execute if score #hp_red mgs.data matches 1.. unless score #hp_blue mgs.data matches 1.. run scoreboard players add #red mgs.mp.team 1

# Blue alone in zone
execute if score #hp_blue mgs.data matches 1.. unless score #hp_red mgs.data matches 1.. at @e[tag=mgs.hp_corner] run playsound minecraft:block.note_block.bell player @a ~ ~ ~ 1 1.2
execute if score #hp_blue mgs.data matches 1.. unless score #hp_red mgs.data matches 1.. run scoreboard players add #blue mgs.mp.team 1

# Check win
execute store result score #score_limit mgs.data run data get storage mgs:multiplayer game.score_limit
execute if score #red mgs.mp.team >= #score_limit mgs.data run function mgs:v5.0.0/multiplayer/team_wins {team:"Red"}
execute if score #blue mgs.mp.team >= #score_limit mgs.data run function mgs:v5.0.0/multiplayer/team_wins {team:"Blue"}

