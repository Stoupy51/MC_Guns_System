
#> mgs:v5.0.0/multiplayer/tp_all_to_spawns
#
# @within	mgs:v5.0.0/multiplayer/start
#

# Copy spawn lists from loaded map
data modify storage mgs:temp _red_spawns set from storage mgs:multiplayer game.map.spawning_points.red
data modify storage mgs:temp _blue_spawns set from storage mgs:multiplayer game.map.spawning_points.blue
data modify storage mgs:temp _general_spawns set from storage mgs:multiplayer game.map.spawning_points.general

# FFA: everyone uses general spawns
execute if data storage mgs:multiplayer game{gamemode:"ffa"} run data modify storage mgs:temp _active_spawns set from storage mgs:temp _general_spawns
execute if data storage mgs:multiplayer game{gamemode:"ffa"} as @a[scores={mgs.mp.in_game=1}] run function mgs:v5.0.0/multiplayer/tp_next_spawn

# Team modes: TP by team
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} run data modify storage mgs:temp _active_spawns set from storage mgs:temp _red_spawns
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} as @a[scores={mgs.mp.in_game=1,mgs.mp.team=1}] run function mgs:v5.0.0/multiplayer/tp_next_spawn

execute unless data storage mgs:multiplayer game{gamemode:"ffa"} run data modify storage mgs:temp _active_spawns set from storage mgs:temp _blue_spawns
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} as @a[scores={mgs.mp.in_game=1,mgs.mp.team=2}] run function mgs:v5.0.0/multiplayer/tp_next_spawn

# Players with no team yet: use general spawns
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} run data modify storage mgs:temp _active_spawns set from storage mgs:temp _general_spawns
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} as @a[scores={mgs.mp.in_game=1,mgs.mp.team=0}] run function mgs:v5.0.0/multiplayer/tp_next_spawn

