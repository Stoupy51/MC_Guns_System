
#> mgs:v5.1.0/missions/game_tick
#
# @within	mgs:v5.1.0/tick
#

# 3 s respawn countdown in real time; range checks, since a 2+ tick delta can jump over an exact 0.
execute as @a[scores={mgs.mi.in_game=1,mgs.mp.spectate_timer=1..}] run scoreboard players operation @s mgs.mp.spectate_timer -= #tick_delta mgs.data
execute as @a[scores={mgs.mi.in_game=1,mgs.mp.spectate_timer=21..40},gamemode=spectator] run title @s subtitle [{"translate":"mgs.respawning_in_2_seconds","color":"gray"}]
execute as @a[scores={mgs.mi.in_game=1,mgs.mp.spectate_timer=1..20},gamemode=spectator] run title @s subtitle [{"translate":"mgs.respawning_in_1_second","color":"gray"}]
# The countdown subtitle is cleared: Minecraft keeps the last subtitle, so a later `title` would show "Respawning in 1 second..." under it.
execute as @a[scores={mgs.mi.in_game=1,mgs.mp.spectate_timer=..0},gamemode=spectator] run title @s subtitle {"text":""}
execute as @a[scores={mgs.mi.in_game=1,mgs.mp.spectate_timer=..0},gamemode=spectator] at @s run function mgs:v5.1.0/missions/actual_respawn

scoreboard players operation #mi_timer mgs.data += #tick_delta mgs.data

# Bounds and OOB for enemies, when the map has a boundary.
execute if score #mi_has_boundary mgs.data matches 1 as @e[tag=mgs.mission_enemy] at @s run function mgs:v5.1.0/shared/check_bounds
execute if score #mi_has_boundary mgs.data matches 1 as @e[type=player,scores={mgs.mi.in_game=1},gamemode=!creative,gamemode=!spectator] at @s run function mgs:v5.1.0/shared/check_bounds
execute as @e[type=player,scores={mgs.mi.in_game=1},gamemode=!creative,gamemode=!spectator] at @s if entity @e[tag=mgs.oob_point,distance=..5] run damage @s 10000 out_of_world

# Enemies drop their weapon at the corpse; drops live for 30 s.
function mgs:v5.1.0/missions/death_watch_tick
# Drops count down in real time and expire.
execute as @e[type=minecraft:item_display,tag=mgs.dropped_gun] run scoreboard players operation @s mgs.drop_timer -= #tick_delta mgs.data
execute as @e[type=minecraft:interaction,tag=mgs.drop_int] run scoreboard players operation @s mgs.drop_timer -= #tick_delta mgs.data
kill @e[type=minecraft:item_display,tag=mgs.dropped_gun,scores={mgs.drop_timer=..0}]
kill @e[type=minecraft:interaction,tag=mgs.drop_int,scores={mgs.drop_timer=..0}]

# Kills = total enemies - alive enemies.
execute store result score #alive mgs.data if entity @e[tag=mgs.mission_enemy]
scoreboard players operation #mi_kills mgs.data = #mi_total_enemies mgs.data
scoreboard players operation #mi_kills mgs.data -= #alive mgs.data

# Every 10 ticks: each update is an item write and a macro parse per player, and a lodestone compass does not need 20 Hz.
scoreboard players operation #mi_compass_phase mgs.data = #total_tick mgs.data
scoreboard players operation #mi_compass_phase mgs.data %= #10 mgs.data
execute if score #alive mgs.data matches 1.. if score #mi_compass_phase mgs.data matches 0 as @a[scores={mgs.mi.in_game=1}] at @s run function mgs:v5.1.0/missions/update_compass

# Around one in-game player (@r would pay a random sort every tick).
execute at @a[scores={mgs.mi.in_game=1},limit=1] run kill @e[type=experience_orb,distance=..200]

function mgs:v5.1.0/shared/maps/call_script_at_base {script:"tick"}

# Reuses #alive from above (a kill from the map tick script is caught a tick later); at least one enemy must have spawned,
# so a broken spawn never ends the game at once.
execute if score #mi_total_enemies mgs.data matches 1.. if score #alive mgs.data matches 0 run return run function mgs:v5.1.0/missions/victory

