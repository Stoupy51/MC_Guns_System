
#> mgs:v5.0.0/zombies/spawn_zombie
#
# @within	mgs:v5.0.0/zombies/spawn_tick
#

# Pick a random zombie spawn point (relative coordinates)
data modify storage mgs:temp _zs_iter set from storage mgs:zombies game.map.spawning_points.zombies

# Count available spawn points
execute store result score #_zs_count mgs.data run data get storage mgs:zombies game.map.spawning_points.zombies
execute if score #_zs_count mgs.data matches ..0 run return fail

# Pick random index
execute store result score #_zs_idx mgs.data run random value 0..100
scoreboard players operation #_zs_idx mgs.data %= #_zs_count mgs.data

# Iterate to that index
function mgs:v5.0.0/zombies/spawn_zombie_at_idx

