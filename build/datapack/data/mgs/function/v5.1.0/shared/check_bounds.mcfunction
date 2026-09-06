
#> mgs:v5.1.0/shared/check_bounds
#
# @executed	as @e[tag=mgs.zombie_round] & at @s
#
# @within	mgs:v5.1.0/zombies/game_tick [ as @e[tag=mgs.zombie_round] & at @s ]
#			mgs:v5.1.0/missions/game_tick [ as @e[tag=mgs.mission_enemy] & at @s ]
#			mgs:v5.1.0/missions/game_tick [ at @s ]
#

execute at @s summon minecraft:marker run function mgs:v5.1.0/shared/probe_pos
execute store result score @s mgs.mp.bx run data get storage mgs:temp _probe_pos[0]
execute store result score @s mgs.mp.by run data get storage mgs:temp _probe_pos[1]
execute store result score @s mgs.mp.bz run data get storage mgs:temp _probe_pos[2]

execute if score @s mgs.mp.bx < #bound_x1 mgs.data run return run damage @s 10000 out_of_world
execute if score @s mgs.mp.bx > #bound_x2 mgs.data run return run damage @s 10000 out_of_world
execute if score @s mgs.mp.by < #bound_y1 mgs.data run return run damage @s 10000 out_of_world
execute if score @s mgs.mp.by > #bound_y2 mgs.data run return run damage @s 10000 out_of_world
execute if score @s mgs.mp.bz < #bound_z1 mgs.data run return run damage @s 10000 out_of_world
execute if score @s mgs.mp.bz > #bound_z2 mgs.data run return run damage @s 10000 out_of_world

## sourceMappingURL=check_bounds.mcfunction.map
