
#> mgs:v5.0.1/zombies/on_stuck_zombie
#
# @executed	as @e[tag=...,limit=24,sort=random] & at @s
#
# @within	mgs:v5.0.1/zombies/stuck_zombie_check
#

# @s = stuck zombie — teleport it to a zombie spawn point near a player instead of killing it
# (keeps the horde intact and drops it back onto walkable navmesh so it can path again).

# Build the rescue pool via the shared spawn-proximity tagger (same 32 -> 64 -> any unlocked
# selection the round spawner uses). #zb_near_found is 0 iff nothing was tagged, so the teleport
# gate below needs no global @e existence scan.
function mgs:v5.0.1/zombies/tag_spawns_near_players

# Teleport to the nearest rescue spawn (passenger death_watch marker follows automatically)
execute if score #zb_near_found mgs.data matches 1.. run tp @s @n[tag=mgs.zb_near]
tag @e[tag=mgs.zb_near] remove mgs.zb_near

# Reset stuck tracking from the new position so it gets a fresh window
scoreboard players set @s mgs.zb.stuck_dist 4
execute store result score @s mgs.zb.stuck_x run data get entity @s Pos[0]
execute store result score @s mgs.zb.stuck_z run data get entity @s Pos[2]
scoreboard players operation @s mgs.zb.stuck_ticks = #total_tick mgs.data

