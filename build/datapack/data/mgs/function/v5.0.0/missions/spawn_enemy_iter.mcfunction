
#> mgs:v5.0.0/missions/spawn_enemy_iter
#
# @within	mgs:v5.0.0/missions/spawn_all_enemies
#			mgs:v5.0.0/missions/spawn_enemy_iter
#

# Read relative position
execute store result score #ex mgs.data run data get storage mgs:temp _enemy_iter[0].pos[0]
execute store result score #ey mgs.data run data get storage mgs:temp _enemy_iter[0].pos[1]
execute store result score #ez mgs.data run data get storage mgs:temp _enemy_iter[0].pos[2]

# Convert to absolute
scoreboard players operation #ex mgs.data += #gm_base_x mgs.data
scoreboard players operation #ey mgs.data += #gm_base_y mgs.data
scoreboard players operation #ez mgs.data += #gm_base_z mgs.data

# Store absolute position for macro
execute store result storage mgs:temp _epos.x double 1 run scoreboard players get #ex mgs.data
execute store result storage mgs:temp _epos.y double 1 run scoreboard players get #ey mgs.data
execute store result storage mgs:temp _epos.z double 1 run scoreboard players get #ez mgs.data

# Copy the function path
data modify storage mgs:temp _epos.function set from storage mgs:temp _enemy_iter[0].function

# Call the mob function at the absolute position
function mgs:v5.0.0/missions/call_enemy_function with storage mgs:temp _epos

# Next
data remove storage mgs:temp _enemy_iter[0]
execute if data storage mgs:temp _enemy_iter[0] run function mgs:v5.0.0/missions/spawn_enemy_iter

