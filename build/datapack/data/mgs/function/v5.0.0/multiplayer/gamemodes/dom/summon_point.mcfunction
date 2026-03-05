
#> mgs:v5.0.0/multiplayer/gamemodes/dom/summon_point
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/dom/setup
#			mgs:v5.0.0/multiplayer/gamemodes/dom/summon_point
#

# Read relative coords
execute store result score #_rx mgs.data run data get storage mgs:temp _dom_iter[0][0]
execute store result score #_ry mgs.data run data get storage mgs:temp _dom_iter[0][1]
execute store result score #_rz mgs.data run data get storage mgs:temp _dom_iter[0][2]

# Add base offset
scoreboard players operation #_rx mgs.data += #gm_base_x mgs.data
scoreboard players operation #_ry mgs.data += #gm_base_y mgs.data
scoreboard players operation #_rz mgs.data += #gm_base_z mgs.data

# Prepare position for macro
execute store result storage mgs:temp _dom_pos.x double 1 run scoreboard players get #_rx mgs.data
execute store result storage mgs:temp _dom_pos.y double 1 run scoreboard players get #_ry mgs.data
execute store result storage mgs:temp _dom_pos.z double 1 run scoreboard players get #_rz mgs.data

# Summon
function mgs:v5.0.0/multiplayer/gamemodes/dom/summon_point_at with storage mgs:temp _dom_pos

# Advance
data remove storage mgs:temp _dom_iter[0]
execute if data storage mgs:temp _dom_iter[0] run function mgs:v5.0.0/multiplayer/gamemodes/dom/summon_point

