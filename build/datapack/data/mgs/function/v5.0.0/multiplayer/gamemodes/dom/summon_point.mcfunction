
#> mgs:v5.0.0/multiplayer/gamemodes/dom/summon_point
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/dom/setup
#			mgs:v5.0.0/multiplayer/gamemodes/dom/summon_point
#

# Read relative coords
execute store result score #rx mgs.data run data get storage mgs:temp _dom_iter[0][0]
execute store result score #ry mgs.data run data get storage mgs:temp _dom_iter[0][1]
execute store result score #rz mgs.data run data get storage mgs:temp _dom_iter[0][2]

# Add base offset
scoreboard players operation #rx mgs.data += #gm_base_x mgs.data
scoreboard players operation #ry mgs.data += #gm_base_y mgs.data
scoreboard players operation #rz mgs.data += #gm_base_z mgs.data

# Prepare position for macro
execute store result storage mgs:temp _dom_pos.x double 1 run scoreboard players get #rx mgs.data
execute store result storage mgs:temp _dom_pos.y double 1 run scoreboard players get #ry mgs.data
execute store result storage mgs:temp _dom_pos.z double 1 run scoreboard players get #rz mgs.data

# Assign zone label (A, B, C, D, E)
execute if score #dom_zone_idx mgs.data matches 0 run data modify storage mgs:temp _dom_pos.label set value "A"
execute if score #dom_zone_idx mgs.data matches 1 run data modify storage mgs:temp _dom_pos.label set value "B"
execute if score #dom_zone_idx mgs.data matches 2 run data modify storage mgs:temp _dom_pos.label set value "C"
execute if score #dom_zone_idx mgs.data matches 3 run data modify storage mgs:temp _dom_pos.label set value "D"
execute if score #dom_zone_idx mgs.data matches 4 run data modify storage mgs:temp _dom_pos.label set value "E"
scoreboard players add #dom_zone_idx mgs.data 1

# Summon marker + text label
function mgs:v5.0.0/multiplayer/gamemodes/dom/summon_point_at with storage mgs:temp _dom_pos

# Advance
data remove storage mgs:temp _dom_iter[0]
execute if data storage mgs:temp _dom_iter[0] run function mgs:v5.0.0/multiplayer/gamemodes/dom/summon_point

