
#> mgs:v5.0.0/shared/load_bounds
#
# @within	mgs:v5.0.0/zombies/start {mode:"zombies"}
#			mgs:v5.0.0/multiplayer/start {mode:"multiplayer"}
#			mgs:v5.0.0/missions/start {mode:"missions"}
#
# @args		mode (string)
#

$execute store result score #bound_x1 mgs.data run data get storage mgs:$(mode) game.map.boundaries[0][0]
$execute store result score #bound_y1 mgs.data run data get storage mgs:$(mode) game.map.boundaries[0][1]
$execute store result score #bound_z1 mgs.data run data get storage mgs:$(mode) game.map.boundaries[0][2]
$execute store result score #bound_x2 mgs.data run data get storage mgs:$(mode) game.map.boundaries[1][0]
$execute store result score #bound_y2 mgs.data run data get storage mgs:$(mode) game.map.boundaries[1][1]
$execute store result score #bound_z2 mgs.data run data get storage mgs:$(mode) game.map.boundaries[1][2]
scoreboard players operation #bound_x1 mgs.data += #gm_base_x mgs.data
scoreboard players operation #bound_y1 mgs.data += #gm_base_y mgs.data
scoreboard players operation #bound_z1 mgs.data += #gm_base_z mgs.data
scoreboard players operation #bound_x2 mgs.data += #gm_base_x mgs.data
scoreboard players operation #bound_y2 mgs.data += #gm_base_y mgs.data
scoreboard players operation #bound_z2 mgs.data += #gm_base_z mgs.data
function mgs:v5.0.0/shared/normalize_bounds

