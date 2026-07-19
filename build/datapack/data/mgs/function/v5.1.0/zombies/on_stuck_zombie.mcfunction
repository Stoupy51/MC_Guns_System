
#> mgs:v5.1.0/zombies/on_stuck_zombie
#
# @executed	as @e[tag=...,limit=24,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/stuck_zombie_check
#			mgs:v5.1.0/zombies/escort/give_up
#

# Prefer a wandering-trader escort over the teleport rescue below (see escort.py).
# Dogs are excluded: the escort freezes its passenger with `data modify entity @s NoAI`, and every
# NBT write on a wolf runs readAdditionalSaveData -> setTame(false,true) -> MAX_HEALTH base reset
# to 8 (TamableAnimal/Wolf). A dog dragged by a taxi arrives at 8 HP, dying to anything it touches.
# They also don't need one — they outrun the trader, so the direct teleport below is strictly better.
execute unless entity @s[tag=mgs.zb_dog] unless entity @s[tag=mgs.zb_escort_failed] if score #zb_escort_count mgs.data matches ..7 run return run function mgs:v5.1.0/zombies/escort/start

# @s = stuck zombie — teleport it to a zombie spawn point near a player instead of killing it
# (keeps the horde intact and drops it back onto walkable navmesh so it can path again).

# Build the rescue pool via the shared spawn-proximity tagger (same 32 -> 64 -> any unlocked
# selection the round spawner uses). #zb_near_found is 0 iff nothing was tagged, so the teleport
# gate below needs no global @e existence scan. Dogs draw from their own markers: a zombie spawn can
# sit somewhere only a walker is meant to come from, and it may not even be inside the play bounds.
execute unless entity @s[tag=mgs.zb_dog] run function mgs:v5.1.0/zombies/tag_spawns_near_players
execute if entity @s[tag=mgs.zb_dog] run function mgs:v5.1.0/zombies/tag_special_spawns_near_players

# Never rescue to the spawn point this zombie last used (initial spawn or previous rescue),
# unless it is the only candidate left.
scoreboard players operation #zb_last_sid mgs.data = @s mgs.zb.spawn.sid
execute as @e[tag=mgs.zb_near] if score @s mgs.zb.spawn.sid = #zb_last_sid mgs.data run tag @s add mgs.zb_near_prev
execute store result score #zb_near_alt mgs.data if entity @e[tag=mgs.zb_near,tag=!mgs.zb_near_prev]
execute if score #zb_near_alt mgs.data matches 1.. run tag @e[tag=mgs.zb_near_prev] remove mgs.zb_near
tag @e[tag=mgs.zb_near_prev] remove mgs.zb_near_prev

# Teleport to the rescue spawn nearest the PLAYER, not the one nearest the stuck enemy. Picking
# from @s meant an enemy stranded far from everyone kept choosing the markers closest to itself,
# and the anti-reuse rule above then bounced it between the same two distant spawns indefinitely.
execute if score #zb_near_found mgs.data matches 1.. at @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] run function mgs:v5.1.0/zombies/rescue_tp
# Everyone downed: no player to measure from, so fall back to the enemy's own position.
execute if score #zb_near_found mgs.data matches 1.. unless entity @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] run function mgs:v5.1.0/zombies/rescue_tp
execute if score #zb_near_found mgs.data matches 1.. run tag @s add mgs.zb_rescued
tag @e[tag=mgs.zb_near] remove mgs.zb_near

# The teleport moved the zombie somewhere new, so a past escort failure no longer applies:
# clear the flag so a future stuck timeout gets a trader again. It only needs to survive long
# enough to route the give_up -> on_stuck_zombie call past the escort router (see escort.py).
execute if score #zb_near_found mgs.data matches 1.. run tag @s remove mgs.zb_escort_failed

# Reset stuck tracking from the new position so it gets a fresh window
scoreboard players set @s mgs.zb.stuck_dist 4
execute store result score @s mgs.zb.stuck_x run data get entity @s Pos[0]
execute store result score @s mgs.zb.stuck_z run data get entity @s Pos[2]
scoreboard players operation @s mgs.zb.stuck_ticks = #total_tick mgs.data

