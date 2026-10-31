
#> mgs:v5.3.0/zombies/summon_spawns
#
# @within	mgs:v5.3.0/zombies/preload_complete
#

# Each marker gets the next unique id.
scoreboard players set #zb_spawn_sid mgs.data 0

data modify storage mgs:temp _spawn_defaults set value {}
data modify storage mgs:temp _spawn_iter set from storage mgs:zombies game.map.spawning_points.players
data modify storage mgs:temp _spawn_tag set value "mgs.spawn_zb_player"
data modify storage mgs:temp _spawn_name set value "Player Spawn"
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.3.0/zombies/summon_spawn_iter

data modify storage mgs:temp _spawn_defaults set value {activation_box:[],walk_to:[],rise_ticks:20,min_round:0,max_round:0,arrival:"floor",power:0b,mob:{entity:"zombie"}}
data modify storage mgs:temp _spawn_iter set from storage mgs:zombies game.map.spawning_points.zombies
data modify storage mgs:temp _spawn_tag set value "mgs.spawn_zb"
data modify storage mgs:temp _spawn_name set value "Zombie Spawn"
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.3.0/zombies/summon_spawn_iter

data modify storage mgs:temp _spawn_defaults set value {activation_box:[],walk_to:[],rise_ticks:20,min_round:0,max_round:0,arrival:"portal",mob:{entity:"wolf"}}
data modify storage mgs:temp _spawn_iter set from storage mgs:zombies game.map.spawning_points.special
data modify storage mgs:temp _spawn_tag set value "mgs.spawn_special"
data modify storage mgs:temp _spawn_name set value "Special Spawn"
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.3.0/zombies/summon_spawn_iter

# game_tick and round completion read both from the first tick.
scoreboard players set #zb_special_round mgs.data 0
scoreboard players set #zb_portal_pending mgs.data 0

# Group 0 is the starting area.
scoreboard players set #unlock_gid mgs.data 0
execute as @e[type=minecraft:marker,tag=mgs.spawn_point] if score @s mgs.zb.spawn.gid = #unlock_gid mgs.data run tag @s add mgs.spawn_unlocked

