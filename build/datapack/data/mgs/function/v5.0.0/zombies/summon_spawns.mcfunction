
#> mgs:v5.0.0/zombies/summon_spawns
#
# @within	mgs:v5.0.0/zombies/preload_complete
#

# Player spawns
data modify storage mgs:temp _spawn_iter set from storage mgs:zombies game.map.spawning_points.players
data modify storage mgs:temp _spawn_tag set value "mgs.spawn_zb_player"
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.0.0/zombies/summon_spawn_iter

# Zombie spawns
data modify storage mgs:temp _spawn_iter set from storage mgs:zombies game.map.spawning_points.zombies
data modify storage mgs:temp _spawn_tag set value "mgs.spawn_zb"
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.0.0/zombies/summon_spawn_iter

# Tag group 0 spawns as unlocked (starting area)
scoreboard players set #_unlock_gid mgs.data 0
execute as @e[tag=mgs.spawn_point] if score @s mgs.zb.spawn.gid = #_unlock_gid mgs.data run tag @s add mgs.spawn_unlocked

