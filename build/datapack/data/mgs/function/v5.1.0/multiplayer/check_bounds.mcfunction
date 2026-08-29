
#> mgs:v5.1.0/multiplayer/check_bounds
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/enforce_bounds
#

# Get player position as integers
execute at @s summon minecraft:marker run function mgs:v5.1.0/shared/probe_pos
execute store result score @s mgs.mp.bx run data get storage mgs:temp _probe_pos[0]
execute store result score @s mgs.mp.by run data get storage mgs:temp _probe_pos[1]
execute store result score @s mgs.mp.bz run data get storage mgs:temp _probe_pos[2]

# Check if outside boundaries (any axis out of range = OOB)
execute if score @s mgs.mp.bx < #bound_x1 mgs.data run return run function mgs:v5.1.0/multiplayer/bounds_kill
execute if score @s mgs.mp.bx > #bound_x2 mgs.data run return run function mgs:v5.1.0/multiplayer/bounds_kill
execute if score @s mgs.mp.by < #bound_y1 mgs.data run return run function mgs:v5.1.0/multiplayer/bounds_kill
execute if score @s mgs.mp.by > #bound_y2 mgs.data run return run function mgs:v5.1.0/multiplayer/bounds_kill
execute if score @s mgs.mp.bz < #bound_z1 mgs.data run return run function mgs:v5.1.0/multiplayer/bounds_kill
execute if score @s mgs.mp.bz > #bound_z2 mgs.data run return run function mgs:v5.1.0/multiplayer/bounds_kill

