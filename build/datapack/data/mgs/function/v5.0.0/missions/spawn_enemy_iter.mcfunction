
#> mgs:v5.0.0/missions/spawn_enemy_iter
#
# @within	mgs:v5.0.0/missions/spawn_level_1
#			mgs:v5.0.0/missions/spawn_level_2
#			mgs:v5.0.0/missions/spawn_level_3
#			mgs:v5.0.0/missions/spawn_level_4
#			mgs:v5.0.0/missions/spawn_enemy_iter
#

# Read relative coordinates
execute store result score #_ex mgs.data run data get storage mgs:temp _enemy_iter[0][0]
execute store result score #_ey mgs.data run data get storage mgs:temp _enemy_iter[0][1]
execute store result score #_ez mgs.data run data get storage mgs:temp _enemy_iter[0][2]

# Convert to absolute
scoreboard players operation #_ex mgs.data += #gm_base_x mgs.data
scoreboard players operation #_ey mgs.data += #gm_base_y mgs.data
scoreboard players operation #_ez mgs.data += #gm_base_z mgs.data

# Store for macro
execute store result storage mgs:temp _epos.x double 1 run scoreboard players get #_ex mgs.data
execute store result storage mgs:temp _epos.y double 1 run scoreboard players get #_ey mgs.data
execute store result storage mgs:temp _epos.z double 1 run scoreboard players get #_ez mgs.data

# Copy entity type and HP from config
data modify storage mgs:temp _epos.entity set from storage mgs:temp _enemy_config.entity
data modify storage mgs:temp _epos.hp set from storage mgs:temp _enemy_config.hp

# Summon
function mgs:v5.0.0/missions/summon_enemy with storage mgs:temp _epos

# Increment enemy count
scoreboard players add #mi_enemies mgs.data 1

# Next
data remove storage mgs:temp _enemy_iter[0]
execute if data storage mgs:temp _enemy_iter[0] run function mgs:v5.0.0/missions/spawn_enemy_iter

