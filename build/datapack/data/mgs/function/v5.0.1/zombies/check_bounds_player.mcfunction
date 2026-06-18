
#> mgs:v5.0.1/zombies/check_bounds_player
#
# @executed	at @s
#
# @within	mgs:v5.0.1/zombies/game_tick [ at @s ]
#

data modify storage mgs:temp _player_pos set from entity @s Pos
execute store result score @s mgs.mp.bx run data get storage mgs:temp _player_pos[0]
execute store result score @s mgs.mp.by run data get storage mgs:temp _player_pos[1]
execute store result score @s mgs.mp.bz run data get storage mgs:temp _player_pos[2]

execute if score @s mgs.mp.bx < #bound_x1 mgs.data run return run function mgs:v5.0.1/zombies/revive/full_death
execute if score @s mgs.mp.bx > #bound_x2 mgs.data run return run function mgs:v5.0.1/zombies/revive/full_death
execute if score @s mgs.mp.by < #bound_y1 mgs.data run return run function mgs:v5.0.1/zombies/revive/full_death
execute if score @s mgs.mp.by > #bound_y2 mgs.data run return run function mgs:v5.0.1/zombies/revive/full_death
execute if score @s mgs.mp.bz < #bound_z1 mgs.data run return run function mgs:v5.0.1/zombies/revive/full_death
execute if score @s mgs.mp.bz > #bound_z2 mgs.data run return run function mgs:v5.0.1/zombies/revive/full_death

