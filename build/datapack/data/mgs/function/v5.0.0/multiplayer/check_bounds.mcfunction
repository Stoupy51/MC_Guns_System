
#> mgs:v5.0.0/multiplayer/check_bounds
#
# @executed	at @s
#
# @within	mgs:v5.0.0/multiplayer/game_tick [ at @s ]
#

# Get player position as integers
data modify storage mgs:temp _player_pos set from entity @s Pos
execute store result score @s mgs.mp.bx run data get storage mgs:temp _player_pos[0]
execute store result score @s mgs.mp.by run data get storage mgs:temp _player_pos[1]
execute store result score @s mgs.mp.bz run data get storage mgs:temp _player_pos[2]

# Check if outside boundaries (any axis out of range = OOB)
execute if score @s mgs.mp.bx < #bound_x1 mgs.data run return run function mgs:v5.0.0/multiplayer/bounds_kill
execute if score @s mgs.mp.bx > #bound_x2 mgs.data run return run function mgs:v5.0.0/multiplayer/bounds_kill
execute if score @s mgs.mp.by < #bound_y1 mgs.data run return run function mgs:v5.0.0/multiplayer/bounds_kill
execute if score @s mgs.mp.by > #bound_y2 mgs.data run return run function mgs:v5.0.0/multiplayer/bounds_kill
execute if score @s mgs.mp.bz < #bound_z1 mgs.data run return run function mgs:v5.0.0/multiplayer/bounds_kill
execute if score @s mgs.mp.bz > #bound_z2 mgs.data run return run function mgs:v5.0.0/multiplayer/bounds_kill

