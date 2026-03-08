
#> mgs:v5.0.0/zombies/summon_spawns
#
# @within	mgs:v5.0.0/zombies/preload_complete
#

# Player spawns
data modify storage mgs:temp _spawn_iter set from storage mgs:zombies game.map.spawning_points.players
data modify storage mgs:temp _spawn_tag set value "mgs.spawn_zb_player"
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.0.0/zombies/summon_spawn_iter

