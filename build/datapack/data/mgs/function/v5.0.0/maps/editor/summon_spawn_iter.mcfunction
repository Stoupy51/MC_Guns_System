
#> mgs:v5.0.0/maps/editor/summon_spawn_iter
#
# @within	mgs:v5.0.0/maps/editor/summon_existing
#			mgs:v5.0.0/maps/editor/summon_spawn_iter
#

# Read relative coordinates from first entry
execute store result score #rx mgs.data run data get storage mgs:temp _spawn_iter[0][0]
execute store result score #ry mgs.data run data get storage mgs:temp _spawn_iter[0][1]
execute store result score #rz mgs.data run data get storage mgs:temp _spawn_iter[0][2]

# Add base to get absolute
scoreboard players operation #rx mgs.data += #base_x mgs.data
scoreboard players operation #ry mgs.data += #base_y mgs.data
scoreboard players operation #rz mgs.data += #base_z mgs.data

# Read yaw
data modify storage mgs:temp _spawn_rot.yaw set from storage mgs:temp _spawn_iter[0][3]

# Prepare position for macro
execute store result storage mgs:temp _spos.x double 1 run scoreboard players get #rx mgs.data
execute store result storage mgs:temp _spos.y double 1 run scoreboard players get #ry mgs.data
execute store result storage mgs:temp _spos.z double 1 run scoreboard players get #rz mgs.data

# Determine tag based on type (1=red, 2=blue, 3=general)
execute if score #_spawn_type mgs.data matches 1 run data modify storage mgs:temp _spos.tag set value "mgs.element.red_spawn"
execute if score #_spawn_type mgs.data matches 2 run data modify storage mgs:temp _spos.tag set value "mgs.element.blue_spawn"
execute if score #_spawn_type mgs.data matches 3 run data modify storage mgs:temp _spos.tag set value "mgs.element.general_spawn"

# Summon marker with yaw stored in data
function mgs:v5.0.0/maps/editor/summon_spawn_marker with storage mgs:temp _spos

# Store rotation data on the marker
execute as @e[tag=mgs.new_spawn_marker,limit=1] run data modify entity @s data.yaw set from storage mgs:temp _spawn_rot.yaw
tag @e[tag=mgs.new_spawn_marker] remove mgs.new_spawn_marker

# Advance to next
data remove storage mgs:temp _spawn_iter[0]
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.0.0/maps/editor/summon_spawn_iter

