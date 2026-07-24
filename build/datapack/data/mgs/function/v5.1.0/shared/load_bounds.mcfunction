
#> mgs:v5.1.0/shared/load_bounds
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/zombies/start {mode:"zombies"}
#			mgs:v5.1.0/multiplayer/start {mode:"multiplayer"}
#			mgs:v5.1.0/missions/start {mode:"missions"}
#
# @args		mode (string)
#

$data modify storage mgs:temp _bnd_corners set from storage mgs:$(mode) game.map.boundaries

# Seed both min (#bound_*1) and max (#bound_*2) from the first corner
execute store result score #bound_x1 mgs.data run data get storage mgs:temp _bnd_corners[0][0]
execute store result score #bound_y1 mgs.data run data get storage mgs:temp _bnd_corners[0][1]
execute store result score #bound_z1 mgs.data run data get storage mgs:temp _bnd_corners[0][2]
scoreboard players operation #bound_x2 mgs.data = #bound_x1 mgs.data
scoreboard players operation #bound_y2 mgs.data = #bound_y1 mgs.data
scoreboard players operation #bound_z2 mgs.data = #bound_z1 mgs.data

# Fold every remaining corner into the running min/max box (already ordered, so no normalize needed)
data remove storage mgs:temp _bnd_corners[0]
execute if data storage mgs:temp _bnd_corners[0] run function mgs:v5.1.0/shared/fold_bounds
data remove storage mgs:temp _bnd_corners

# Offset the whole box by the map base (corners are stored relative to it)
scoreboard players operation #bound_x1 mgs.data += #gm_base_x mgs.data
scoreboard players operation #bound_y1 mgs.data += #gm_base_y mgs.data
scoreboard players operation #bound_z1 mgs.data += #gm_base_z mgs.data
scoreboard players operation #bound_x2 mgs.data += #gm_base_x mgs.data
scoreboard players operation #bound_y2 mgs.data += #gm_base_y mgs.data
scoreboard players operation #bound_z2 mgs.data += #gm_base_z mgs.data

