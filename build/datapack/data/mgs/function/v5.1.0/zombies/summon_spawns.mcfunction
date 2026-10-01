
#> mgs:v5.1.0/zombies/summon_spawns
#
# @within	mgs:v5.1.0/zombies/preload_complete
#

# Each marker gets the next unique id.
scoreboard players set #zb_spawn_sid mgs.data 0

data modify storage mgs:temp _spawn_iter set from storage mgs:zombies game.map.spawning_points.players
data modify storage mgs:temp _spawn_tag set value "mgs.spawn_zb_player"
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.1.0/zombies/summon_spawn_iter

data modify storage mgs:temp _spawn_iter set from storage mgs:zombies game.map.spawning_points.zombies
data modify storage mgs:temp _spawn_tag set value "mgs.spawn_zb"
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.1.0/zombies/summon_spawn_iter

# Special spawns (dog rounds, later mini-bosses) work like zombie spawns; only the tag differs.
data modify storage mgs:temp _spawn_iter set from storage mgs:zombies game.map.spawning_points.special
data modify storage mgs:temp _spawn_tag set value "mgs.spawn_special"
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.1.0/zombies/summon_spawn_iter

# From the map data, not an entity scan, so start_round gates dog rounds on a score.
execute store success score #zb_has_special mgs.data if data storage mgs:zombies game.map.spawning_points.special[0]

# game_tick and round completion read both flags from the first tick.
scoreboard players set #zb_dog_round mgs.data 0
scoreboard players set #zb_dog_pending mgs.data 0

# Group 0 is the starting area.
scoreboard players set #unlock_gid mgs.data 0
execute as @e[tag=mgs.spawn_point] if score @s mgs.zb.spawn.gid = #unlock_gid mgs.data run tag @s add mgs.spawn_unlocked

