
#> mgs:v5.1.0/missions/game_tick
#
# @within	mgs:v5.1.0/tick
#

# Spectate Timer (3s respawn cooldown, real-time via #tick_delta).
# Range checks instead of exact values: a 2+ tick delta under lag can jump over any single value
# (an exact =0 respawn check would then never fire)
execute as @a[scores={mgs.mi.in_game=1,mgs.mp.spectate_timer=1..}] run scoreboard players operation @s mgs.mp.spectate_timer -= #tick_delta mgs.data
execute as @a[scores={mgs.mi.in_game=1,mgs.mp.spectate_timer=21..40},gamemode=spectator] run title @s subtitle [{"translate":"mgs.respawning_in_2_seconds","color":"gray"}]
execute as @a[scores={mgs.mi.in_game=1,mgs.mp.spectate_timer=1..20},gamemode=spectator] run title @s subtitle [{"translate":"mgs.respawning_in_1_second","color":"gray"}]
# Clear the countdown subtitle on respawn: Minecraft keeps the last subtitle until something
# replaces it, so any later `title` (a round banner, the hit indicator) would redisplay a stale
# "Respawning in 1 second..." underneath it.
execute as @a[scores={mgs.mi.in_game=1,mgs.mp.spectate_timer=..0},gamemode=spectator] run title @s subtitle {"text":""}
execute as @a[scores={mgs.mi.in_game=1,mgs.mp.spectate_timer=..0},gamemode=spectator] at @s run function mgs:v5.1.0/missions/actual_respawn

# Increment mission timer
scoreboard players operation #mi_timer mgs.data += #tick_delta mgs.data

# Boundary enforcement (skip spectators) & OOB Check
execute if score #mi_has_boundary mgs.data matches 1 as @e[tag=mgs.mission_enemy] at @s run function mgs:v5.1.0/shared/check_bounds
execute if score #mi_has_boundary mgs.data matches 1 as @e[type=player,scores={mgs.mi.in_game=1},gamemode=!creative,gamemode=!spectator] at @s run function mgs:v5.1.0/shared/check_bounds
execute as @e[type=player,scores={mgs.mi.in_game=1},gamemode=!creative,gamemode=!spectator] at @s if entity @e[tag=mgs.oob_point,distance=..5] run damage @s 10000 out_of_world

# Enemies drop their weapon at the corpse; the drops then live for 30s
function mgs:v5.1.0/missions/death_watch_tick
# Dropped-weapon lifetime: count down (real-time via #tick_delta) and remove expired drops
execute as @e[type=minecraft:item_display,tag=mgs.dropped_gun] run scoreboard players operation @s mgs.drop_timer -= #tick_delta mgs.data
execute as @e[type=minecraft:interaction,tag=mgs.drop_int] run scoreboard players operation @s mgs.drop_timer -= #tick_delta mgs.data
kill @e[type=minecraft:item_display,tag=mgs.dropped_gun,scores={mgs.drop_timer=..0}]
kill @e[type=minecraft:interaction,tag=mgs.drop_int,scores={mgs.drop_timer=..0}]

# Track enemy kills (total enemies - alive enemies)
execute store result score #alive mgs.data if entity @e[tag=mgs.mission_enemy]
scoreboard players operation #mi_kills mgs.data = #mi_total_enemies mgs.data
scoreboard players operation #mi_kills mgs.data -= #alive mgs.data

# Update compass for all players every 10 ticks (points to nearest enemy — each update is an
# item write + macro parse per player, and a lodestone compass doesn't need 20Hz retargeting)
scoreboard players operation #mi_compass_phase mgs.data = #total_tick mgs.data
scoreboard players operation #mi_compass_phase mgs.data %= #10 mgs.data
execute if score #alive mgs.data matches 1.. if score #mi_compass_phase mgs.data matches 0 as @a[scores={mgs.mi.in_game=1}] at @s run function mgs:v5.1.0/missions/update_compass

# Orb cleanup around any one in-game player (@r paid a random sort every tick for nothing)
execute at @a[scores={mgs.mi.in_game=1},limit=1] run kill @e[type=experience_orb,distance=..200]

# Call map-defined tick script
function mgs:v5.1.0/shared/maps/call_tick_script_at_base

# Check if all enemies are dead → victory (reuses #alive counted above instead of a second
# full-entity scan; a kill from the map tick script above is caught one tick later).
# Requires at least one spawned enemy so a broken spawn can never instantly end the game.
execute if score #mi_total_enemies mgs.data matches 1.. if score #alive mgs.data matches 0 run return run function mgs:v5.1.0/missions/victory

