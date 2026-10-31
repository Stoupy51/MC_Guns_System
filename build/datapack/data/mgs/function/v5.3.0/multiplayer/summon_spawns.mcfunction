
#> mgs:v5.3.0/multiplayer/summon_spawns
#
# @executed	as the player & at current position
#
# @within	mgs:v5.3.0/multiplayer/start
#

data modify storage mgs:temp _spawn_iter set from storage mgs:multiplayer game.map.spawning_points.red
data modify storage mgs:temp _spawn_tag set value "mgs.spawn_red"
data modify storage mgs:temp _spawn_name set value "Red Spawn"
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.3.0/multiplayer/summon_spawn_iter

data modify storage mgs:temp _spawn_iter set from storage mgs:multiplayer game.map.spawning_points.blue
data modify storage mgs:temp _spawn_tag set value "mgs.spawn_blue"
data modify storage mgs:temp _spawn_name set value "Blue Spawn"
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.3.0/multiplayer/summon_spawn_iter

data modify storage mgs:temp _spawn_iter set from storage mgs:multiplayer game.map.spawning_points.general
data modify storage mgs:temp _spawn_tag set value "mgs.spawn_general"
data modify storage mgs:temp _spawn_name set value "General Spawn"
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.3.0/multiplayer/summon_spawn_iter

