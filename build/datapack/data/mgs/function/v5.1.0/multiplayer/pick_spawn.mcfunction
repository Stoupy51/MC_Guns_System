
#> mgs:v5.1.0/multiplayer/pick_spawn
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/tp_all_to_spawns {type:"general"} [ at @s ]
#			mgs:v5.1.0/multiplayer/tp_all_to_spawns {type:"red"} [ at @s ]
#			mgs:v5.1.0/multiplayer/tp_all_to_spawns {type:"blue"} [ at @s ]
#			mgs:v5.1.0/multiplayer/respawn_tp {type:"general"}
#			mgs:v5.1.0/multiplayer/respawn_tp {type:"red"}
#			mgs:v5.1.0/multiplayer/respawn_tp {type:"blue"}
#			mgs:v5.1.0/multiplayer/gamemodes/snd/start_round {type:"red"} [ as @a[scores={mgs.mp.team=1}] & at @s ]
#			mgs:v5.1.0/multiplayer/gamemodes/snd/start_round {type:"blue"} [ as @a[scores={mgs.mp.team=2}] & at @s ]
#			mgs:v5.1.0/multiplayer/gamemodes/demo/start_round {type:"red"} [ as @a[scores={mgs.mp.team=1}] & at @s ]
#			mgs:v5.1.0/multiplayer/gamemodes/demo/start_round {type:"blue"} [ as @a[scores={mgs.mp.team=2}] & at @s ]
#
# @args		type (string)
#

tag @s add mgs.spawn_pending

# FFA or team 0: every other in-game player is an enemy.
execute if score @s mgs.mp.team matches 0 run tag @a[scores={mgs.mp.in_game=1}] add mgs.spawn_enemy
# Team modes: only the other team.
execute if score @s mgs.mp.team matches 1 run tag @a[scores={mgs.mp.in_game=1,mgs.mp.team=2..}] add mgs.spawn_enemy
execute if score @s mgs.mp.team matches 2 run tag @a[scores={mgs.mp.in_game=1,mgs.mp.team=..1}] add mgs.spawn_enemy
tag @s remove mgs.spawn_enemy

# #mp_cand_count follows the tagged candidates, so the "all contested" fallback tests a score instead of scanning @e.
$execute store result score #mp_cand_count mgs.data run tag @e[tag=mgs.spawn_point,tag=mgs.spawn_$(type),tag=!mgs.spawn_used] add mgs.spawn_candidate

# Drop candidates with an enemy within 5 blocks.
execute as @e[tag=mgs.spawn_candidate] at @s if entity @a[tag=mgs.spawn_enemy,distance=..5] run function mgs:v5.1.0/multiplayer/uncontest_spawn

# All used or contested: every spawn of the type is a candidate again.
$execute if score #mp_cand_count mgs.data matches 0 run tag @e[tag=mgs.spawn_point,tag=mgs.spawn_$(type)] add mgs.spawn_candidate

# No enemies: any candidate, without the distance computation.
execute unless entity @a[tag=mgs.spawn_enemy] run return run function mgs:v5.1.0/multiplayer/pick_spawn_random

# At most 32 random candidates get the distance computation.
tag @e[tag=mgs.spawn_candidate,sort=random,limit=32] add mgs.spawn_final
tag @e[tag=mgs.spawn_candidate,tag=!mgs.spawn_final] remove mgs.spawn_candidate
tag @e[tag=mgs.spawn_final] remove mgs.spawn_final

# Squared distance to the nearest enemy.
execute as @e[tag=mgs.spawn_candidate] at @s run function mgs:v5.1.0/multiplayer/spawn_calc_dist

scoreboard players set #best_dist mgs.data 0
scoreboard players operation #best_dist mgs.data > @e[tag=mgs.spawn_candidate] mgs.data

# A random one among the farthest.
execute as @e[tag=mgs.spawn_candidate,sort=random] if score @s mgs.data = #best_dist mgs.data run function mgs:v5.1.0/shared/tp_to_spawn {mode:"multiplayer"}

tag @e[tag=mgs.spawn_candidate] remove mgs.spawn_candidate
tag @a[tag=mgs.spawn_pending] remove mgs.spawn_pending
tag @a[tag=mgs.spawn_enemy] remove mgs.spawn_enemy

