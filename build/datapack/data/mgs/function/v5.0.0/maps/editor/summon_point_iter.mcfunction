
#> mgs:v5.0.0/maps/editor/summon_point_iter
#
# @within	mgs:v5.0.0/maps/editor/summon_existing/multiplayer
#			mgs:v5.0.0/maps/editor/summon_existing/missions
#			mgs:v5.0.0/maps/editor/summon_point_iter
#

# Read relative coordinates
execute store result score #rx mgs.data run data get storage mgs:temp _point_iter[0][0]
execute store result score #ry mgs.data run data get storage mgs:temp _point_iter[0][1]
execute store result score #rz mgs.data run data get storage mgs:temp _point_iter[0][2]

# Add base
scoreboard players operation #rx mgs.data += #base_x mgs.data
scoreboard players operation #ry mgs.data += #base_y mgs.data
scoreboard players operation #rz mgs.data += #base_z mgs.data

# Prepare position
execute store result storage mgs:temp _ppos.x double 1 run scoreboard players get #rx mgs.data
execute store result storage mgs:temp _ppos.y double 1 run scoreboard players get #ry mgs.data
execute store result storage mgs:temp _ppos.z double 1 run scoreboard players get #rz mgs.data

# Set tag from stored tag
data modify storage mgs:temp _ppos.tag set from storage mgs:temp _point_iter_tag

function mgs:v5.0.0/maps/editor/summon_point_marker with storage mgs:temp _ppos

# Advance
data remove storage mgs:temp _point_iter[0]
execute if data storage mgs:temp _point_iter[0] run function mgs:v5.0.0/maps/editor/summon_point_iter

