
#> mgs:v5.0.0/multiplayer/tp_all_to_spawns
#
# @within	mgs:v5.0.0/multiplayer/start
#

# FFA: everyone uses general spawns
execute if data storage mgs:multiplayer game{gamemode:"ffa"} as @a[scores={mgs.mp.in_game=1}] at @s run function mgs:v5.0.0/multiplayer/pick_spawn {type:"general"}

# Team modes: TP by team
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} as @a[scores={mgs.mp.in_game=1,mgs.mp.team=1}] at @s run function mgs:v5.0.0/multiplayer/pick_spawn {type:"red"}
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} as @a[scores={mgs.mp.in_game=1,mgs.mp.team=2}] at @s run function mgs:v5.0.0/multiplayer/pick_spawn {type:"blue"}

# Players with no team: use general spawns
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} as @a[scores={mgs.mp.in_game=1,mgs.mp.team=0}] at @s run function mgs:v5.0.0/multiplayer/pick_spawn {type:"general"}

