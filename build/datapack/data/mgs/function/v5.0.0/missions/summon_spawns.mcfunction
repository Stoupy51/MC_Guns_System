
#> mgs:v5.0.0/missions/summon_spawns
#
# @within	mgs:v5.0.0/missions/preload_complete
#

# Mission spawns
data modify storage mgs:temp _spawn_iter set from storage mgs:missions game.map.spawning_points.mission
data modify storage mgs:temp _spawn_tag set value "mgs.spawn_mission"
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.0.0/missions/summon_spawn_iter

