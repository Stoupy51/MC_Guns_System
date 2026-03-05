
#> mgs:v5.0.0/multiplayer/summon_spawns
#
# @within	mgs:v5.0.0/multiplayer/start
#

# Red spawns
data modify storage mgs:temp _spawn_iter set from storage mgs:multiplayer game.map.spawning_points.red
data modify storage mgs:temp _spawn_tag set value "mgs.spawn_red"
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.0.0/multiplayer/summon_spawn_iter

# Blue spawns
data modify storage mgs:temp _spawn_iter set from storage mgs:multiplayer game.map.spawning_points.blue
data modify storage mgs:temp _spawn_tag set value "mgs.spawn_blue"
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.0.0/multiplayer/summon_spawn_iter

# General spawns
data modify storage mgs:temp _spawn_iter set from storage mgs:multiplayer game.map.spawning_points.general
data modify storage mgs:temp _spawn_tag set value "mgs.spawn_general"
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.0.0/multiplayer/summon_spawn_iter

