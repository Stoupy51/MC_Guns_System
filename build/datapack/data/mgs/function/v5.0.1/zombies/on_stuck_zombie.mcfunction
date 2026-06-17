
#> mgs:v5.0.1/zombies/on_stuck_zombie
#
# @executed	as @e[tag=...,limit=24,sort=random] & at @s
#
# @within	mgs:v5.0.1/zombies/stuck_zombie_check
#

# @s = stuck zombie — teleport it to a zombie spawn point near a player instead of killing it
# (keeps the horde intact and drops it back onto walkable navmesh so it can path again).

# Build the rescue pool: unlocked zombie spawn markers near any in-game player — same selection
# the spawner uses (within 32, widening to 64, then any unlocked spawn as a final fallback).
tag @e[tag=mgs.spawn_zb] remove mgs.zb_rescue
execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] at @s run tag @e[tag=mgs.spawn_zb,tag=mgs.spawn_unlocked,distance=..32] add mgs.zb_rescue
execute unless entity @e[tag=mgs.zb_rescue] as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] at @s run tag @e[tag=mgs.spawn_zb,tag=mgs.spawn_unlocked,distance=..64] add mgs.zb_rescue
execute unless entity @e[tag=mgs.zb_rescue] run tag @e[tag=mgs.spawn_zb,tag=mgs.spawn_unlocked] add mgs.zb_rescue

# Teleport to the nearest rescue spawn (passenger death_watch marker follows automatically)
execute if entity @e[tag=mgs.zb_rescue] run tp @s @n[tag=mgs.zb_rescue]
tag @e[tag=mgs.zb_rescue] remove mgs.zb_rescue

# Reset stuck tracking from the new position so it gets a fresh window
scoreboard players set @s mgs.zb.stuck_dist 4
execute store result score @s mgs.zb.stuck_x run data get entity @s Pos[0]
execute store result score @s mgs.zb.stuck_z run data get entity @s Pos[2]
scoreboard players operation @s mgs.zb.stuck_ticks = #total_tick mgs.data

