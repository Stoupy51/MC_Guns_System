
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

# Never rescue to the spawn point this zombie last used (initial spawn or previous rescue),
# unless it is the only candidate left.
scoreboard players operation #zb_last_sid mgs.data = @s mgs.zb.spawn.sid
execute as @e[tag=mgs.zb_near] if score @s mgs.zb.spawn.sid = #zb_last_sid mgs.data run tag @s add mgs.zb_near_prev
execute store result score #zb_near_alt mgs.data if entity @e[tag=mgs.zb_near,tag=!mgs.zb_near_prev]
execute if score #zb_near_alt mgs.data matches 1.. run tag @e[tag=mgs.zb_near_prev] remove mgs.zb_near
tag @e[tag=mgs.zb_near_prev] remove mgs.zb_near_prev

# Teleport to the nearest rescue spawn (passenger death_watch marker follows automatically),
# remember its id, and flag the zombie as rescued (shortens the next "not moved" timeout to 5s)
execute if score #zb_near_found mgs.data matches 1.. run tp @s @n[tag=mgs.zb_near]
execute if score #zb_near_found mgs.data matches 1.. run scoreboard players operation @s mgs.zb.spawn.sid = @n[tag=mgs.zb_near] mgs.zb.spawn.sid
execute if score #zb_near_found mgs.data matches 1.. run tag @s add mgs.zb_rescued
tag @e[tag=mgs.zb_near] remove mgs.zb_near

# Reset stuck tracking from the new position so it gets a fresh window
scoreboard players set @s mgs.zb.stuck_dist 4
execute store result score @s mgs.zb.stuck_x run data get entity @s Pos[0]
execute store result score @s mgs.zb.stuck_z run data get entity @s Pos[2]
scoreboard players operation @s mgs.zb.stuck_ticks = #total_tick mgs.data

