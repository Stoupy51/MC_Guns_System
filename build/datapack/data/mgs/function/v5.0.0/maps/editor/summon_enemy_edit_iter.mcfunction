
#> mgs:v5.0.0/maps/editor/summon_enemy_edit_iter
#
# @within	mgs:v5.0.0/maps/editor/summon_existing/missions
#			mgs:v5.0.0/maps/editor/summon_enemy_edit_iter
#

# Read relative position from first entry
execute store result score #rx mgs.data run data get storage mgs:temp _enemy_edit_iter[0].pos[0]
execute store result score #ry mgs.data run data get storage mgs:temp _enemy_edit_iter[0].pos[1]
execute store result score #rz mgs.data run data get storage mgs:temp _enemy_edit_iter[0].pos[2]

# Add base to get absolute
scoreboard players operation #rx mgs.data += #base_x mgs.data
scoreboard players operation #ry mgs.data += #base_y mgs.data
scoreboard players operation #rz mgs.data += #base_z mgs.data

# Prepare position for macro
execute store result storage mgs:temp _epos.x double 1 run scoreboard players get #rx mgs.data
execute store result storage mgs:temp _epos.y double 1 run scoreboard players get #ry mgs.data
execute store result storage mgs:temp _epos.z double 1 run scoreboard players get #rz mgs.data

# Summon marker
function mgs:v5.0.0/maps/editor/summon_enemy_marker with storage mgs:temp _epos

# Store function data on the marker
execute as @n[tag=mgs.new_enemy_marker] run data modify entity @s data.function set from storage mgs:temp _enemy_edit_iter[0].function
tag @e[tag=mgs.new_enemy_marker] remove mgs.new_enemy_marker

# Advance to next
data remove storage mgs:temp _enemy_edit_iter[0]
execute if data storage mgs:temp _enemy_edit_iter[0] run function mgs:v5.0.0/maps/editor/summon_enemy_edit_iter

