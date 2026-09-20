
#> mgs:v5.1.0/shared/tp_to_spawn
#
# @executed	as @n[tag=mgs.spawn_candidate,sort=random]
#
# @within	mgs:v5.1.0/zombies/pick_spawn {mode:"zombies"} [ as @n[tag=mgs.spawn_candidate,sort=random] ]
#			mgs:v5.1.0/zombies/whos_who/on_down {mode:"zombies"} [ as @n[tag=mgs.spawn_candidate] ]
#			mgs:v5.1.0/zombies/revive/respawn_near_player {mode:"zombies"} [ as @n[tag=mgs.spawn_candidate] ]
#			mgs:v5.1.0/multiplayer/pick_spawn {mode:"multiplayer"} [ as @e[tag=mgs.spawn_candidate,sort=random] ]
#			mgs:v5.1.0/multiplayer/pick_spawn_random {mode:"multiplayer"} [ as @n[tag=mgs.spawn_candidate,sort=random] ]
#			mgs:v5.1.0/missions/pick_spawn {mode:"missions"} [ as @n[tag=mgs.spawn_candidate,sort=random] ]
#
# @args		mode (string)
#

# Store marker position and yaw for the teleport macro
execute store result storage mgs:temp _tp.x double 1 run data get entity @s Pos[0]
execute store result storage mgs:temp _tp.y double 1 run data get entity @s Pos[1]
execute store result storage mgs:temp _tp.z double 1 run data get entity @s Pos[2]
data modify storage mgs:temp _tp.yaw set from entity @s data.yaw

# TP the pending player
execute as @p[tag=mgs.spawn_pending] run function mgs:v5.1.0/shared/tp_player_at with storage mgs:temp _tp

# Mark this spawn as used (prevents duplicate assignments) (only in preparing time)
$execute unless data storage mgs:$(mode) game{state:"active"} run tag @s add mgs.spawn_used

