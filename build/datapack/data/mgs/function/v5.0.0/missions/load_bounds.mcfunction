
#> mgs:v5.0.0/missions/load_bounds
#
# @within	mgs:v5.0.0/missions/start
#

execute store result score #bound_x1 mgs.data run data get storage mgs:missions game.map.boundaries[0][0]
execute store result score #bound_y1 mgs.data run data get storage mgs:missions game.map.boundaries[0][1]
execute store result score #bound_z1 mgs.data run data get storage mgs:missions game.map.boundaries[0][2]
execute store result score #bound_x2 mgs.data run data get storage mgs:missions game.map.boundaries[1][0]
execute store result score #bound_y2 mgs.data run data get storage mgs:missions game.map.boundaries[1][1]
execute store result score #bound_z2 mgs.data run data get storage mgs:missions game.map.boundaries[1][2]
scoreboard players operation #bound_x1 mgs.data += #gm_base_x mgs.data
scoreboard players operation #bound_y1 mgs.data += #gm_base_y mgs.data
scoreboard players operation #bound_z1 mgs.data += #gm_base_z mgs.data
scoreboard players operation #bound_x2 mgs.data += #gm_base_x mgs.data
scoreboard players operation #bound_y2 mgs.data += #gm_base_y mgs.data
scoreboard players operation #bound_z2 mgs.data += #gm_base_z mgs.data
function mgs:v5.0.0/missions/normalize_bounds

