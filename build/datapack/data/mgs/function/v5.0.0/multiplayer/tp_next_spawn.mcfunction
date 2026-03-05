
#> mgs:v5.0.0/multiplayer/tp_next_spawn
#
# @executed	as @a[scores={mgs.mp.in_game=1}]
#
# @within	mgs:v5.0.0/multiplayer/tp_all_to_spawns [ as @a[scores={mgs.mp.in_game=1}] ]
#			mgs:v5.0.0/multiplayer/tp_all_to_spawns [ as @a[scores={mgs.mp.in_game=1,mgs.mp.team=1}] ]
#			mgs:v5.0.0/multiplayer/tp_all_to_spawns [ as @a[scores={mgs.mp.in_game=1,mgs.mp.team=2}] ]
#			mgs:v5.0.0/multiplayer/tp_all_to_spawns [ as @a[scores={mgs.mp.in_game=1,mgs.mp.team=0}] ]
#

# Read first spawn point coords (relative)
execute store result score #_sx mgs.data run data get storage mgs:temp _active_spawns[0][0]
execute store result score #_sy mgs.data run data get storage mgs:temp _active_spawns[0][1]
execute store result score #_sz mgs.data run data get storage mgs:temp _active_spawns[0][2]
execute store result score #_syaw mgs.data run data get storage mgs:temp _active_spawns[0][3] 100

# Add base offset → absolute coords
scoreboard players operation #_sx mgs.data += #gm_base_x mgs.data
scoreboard players operation #_sy mgs.data += #gm_base_y mgs.data
scoreboard players operation #_sz mgs.data += #gm_base_z mgs.data

# Store for macro
execute store result storage mgs:temp _tp.x double 1 run scoreboard players get #_sx mgs.data
execute store result storage mgs:temp _tp.y double 1 run scoreboard players get #_sy mgs.data
execute store result storage mgs:temp _tp.z double 1 run scoreboard players get #_sz mgs.data
execute store result storage mgs:temp _tp.yaw double 0.01 run scoreboard players get #_syaw mgs.data

# Rotate list: move first to end, then remove first
data modify storage mgs:temp _active_spawns append from storage mgs:temp _active_spawns[0]
data remove storage mgs:temp _active_spawns[0]

# TP
function mgs:v5.0.0/multiplayer/tp_player_at with storage mgs:temp _tp

