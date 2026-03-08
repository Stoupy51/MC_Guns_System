
#> mgs:v5.0.0/maps/editor/summon_zb_object_iter
#
# @within	mgs:v5.0.0/maps/editor/summon_existing/zombies
#			mgs:v5.0.0/maps/editor/summon_zb_object_iter
#

# Read relative position from first entry
execute store result score #rx mgs.data run data get storage mgs:temp _zb_iter[0].pos[0]
execute store result score #ry mgs.data run data get storage mgs:temp _zb_iter[0].pos[1]
execute store result score #rz mgs.data run data get storage mgs:temp _zb_iter[0].pos[2]

# Add base to get absolute
scoreboard players operation #rx mgs.data += #base_x mgs.data
scoreboard players operation #ry mgs.data += #base_y mgs.data
scoreboard players operation #rz mgs.data += #base_z mgs.data

# Prepare position for macro
execute store result storage mgs:temp _zbpos.x double 1 run scoreboard players get #rx mgs.data
execute store result storage mgs:temp _zbpos.y double 1 run scoreboard players get #ry mgs.data
execute store result storage mgs:temp _zbpos.z double 1 run scoreboard players get #rz mgs.data

# Set tag
data modify storage mgs:temp _zbpos.tag set from storage mgs:temp _zb_iter_tag

# Summon marker
function mgs:v5.0.0/maps/editor/summon_zb_marker with storage mgs:temp _zbpos

# Copy all compound data onto the marker
execute as @n[tag=mgs.new_zb_marker] run data modify entity @s data set from storage mgs:temp _zb_iter[0]

# Set yaw from rotation for the direction indicator
execute if data storage mgs:temp _zb_iter[0].rotation run execute as @n[tag=mgs.new_zb_marker] run data modify entity @s data.yaw set from storage mgs:temp _zb_iter[0].rotation[0]

tag @e[tag=mgs.new_zb_marker] remove mgs.new_zb_marker

# Advance to next
data remove storage mgs:temp _zb_iter[0]
execute if data storage mgs:temp _zb_iter[0] run function mgs:v5.0.0/maps/editor/summon_zb_object_iter

