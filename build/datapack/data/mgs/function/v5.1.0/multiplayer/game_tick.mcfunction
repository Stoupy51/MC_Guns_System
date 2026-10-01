
#> mgs:v5.1.0/multiplayer/game_tick
#
# @within	mgs:v5.1.0/tick
#

# The XP bar is the progression HUD, so a stray orb would show a level nobody earned; tick_player re-asserts the bar every second.
kill @e[type=experience_orb]

# Spectate Timer (3s respawn cooldown, real-time via #tick_delta).
# Range checks instead of exact values: a 2+ tick delta under lag can jump over any single value
# (an exact =0 respawn check would then never fire)
execute as @a[scores={mgs.mp.in_game=1,mgs.mp.spectate_timer=1..}] run scoreboard players operation @s mgs.mp.spectate_timer -= #tick_delta mgs.data
execute as @a[scores={mgs.mp.in_game=1,mgs.mp.spectate_timer=21..40},gamemode=spectator] run title @s subtitle [{"translate":"mgs.respawning_in_2_seconds","color":"gray"}]
execute as @a[scores={mgs.mp.in_game=1,mgs.mp.spectate_timer=1..20},gamemode=spectator] run title @s subtitle [{"translate":"mgs.respawning_in_1_second","color":"gray"}]
# Clear the countdown subtitle on respawn: Minecraft keeps the last subtitle until something
# replaces it, so any later `title` (a round banner, the hit indicator) would redisplay a stale
# "Respawning in 1 second..." underneath it.
execute as @a[scores={mgs.mp.in_game=1,mgs.mp.spectate_timer=..0},gamemode=spectator] run title @s subtitle {"text":""}
execute as @a[scores={mgs.mp.in_game=1,mgs.mp.spectate_timer=..0},gamemode=spectator] at @s run function mgs:v5.1.0/multiplayer/actual_respawn

# Dropped-weapon lifetime: count down (real-time via #tick_delta) and remove expired drops
execute as @e[type=minecraft:item_display,tag=mgs.dropped_gun] run scoreboard players operation @s mgs.drop_timer -= #tick_delta mgs.data
execute as @e[type=minecraft:interaction,tag=mgs.drop_int] run scoreboard players operation @s mgs.drop_timer -= #tick_delta mgs.data
kill @e[type=minecraft:item_display,tag=mgs.dropped_gun,scores={mgs.drop_timer=..0}]
kill @e[type=minecraft:interaction,tag=mgs.drop_int,scores={mgs.drop_timer=..0}]

# Real time through #tick_delta, unless the gamemode claimed #mp_timer in its setup: round-based modes drive it from their own clock
# (S&D round timer then fuse, Demolition plant-aware clock), since a match-wide limit cannot judge a best-of-N format.
execute if score #mp_mode_owns_timer mgs.data matches 0 run scoreboard players operation #mp_timer mgs.data -= #tick_delta mgs.data

# Keyed to #total_tick: under lag #tick_delta can jump past a `#mp_timer % 20` hit.
execute store result score #tick_mod mgs.data run scoreboard players get #total_tick mgs.data
scoreboard players operation #tick_mod mgs.data %= #20 mgs.data
execute if score #tick_mod mgs.data matches 0 run function mgs:v5.1.0/multiplayer/timer_display

# Never for a mode that owns the score, where 0 is a round event it handles.
execute if score #mp_mode_owns_timer mgs.data matches 0 if score #mp_timer mgs.data matches ..0 run function mgs:v5.1.0/multiplayer/time_up

# See multiplayer/enforce_bounds.
execute store result score #bounds_phase mgs.data run scoreboard players get #total_tick mgs.data
scoreboard players operation #bounds_phase mgs.data %= #4 mgs.data

# Bounds and OOB markers in one scan, skipping respawn-protected and non-playing players.
execute as @e[type=player,scores={mgs.mp.in_game=1,mgs.mp.death_count=0},gamemode=!creative,gamemode=!spectator] at @s run function mgs:v5.1.0/multiplayer/enforce_bounds

execute if data storage mgs:multiplayer game{gamemode:"ffa"} run function mgs:v5.1.0/multiplayer/gamemodes/ffa/tick
execute if data storage mgs:multiplayer game{gamemode:"tdm"} run function mgs:v5.1.0/multiplayer/gamemodes/tdm/tick
execute if data storage mgs:multiplayer game{gamemode:"dom"} run function mgs:v5.1.0/multiplayer/gamemodes/dom/tick
execute if data storage mgs:multiplayer game{gamemode:"hp"} run function mgs:v5.1.0/multiplayer/gamemodes/hp/tick
execute if data storage mgs:multiplayer game{gamemode:"snd"} run function mgs:v5.1.0/multiplayer/gamemodes/snd/tick
execute if data storage mgs:multiplayer game{gamemode:"demo"} run function mgs:v5.1.0/multiplayer/gamemodes/demo/tick

# Tracker perk: enemy footprints every 6 ticks.
execute store result score #tick_mod mgs.data run scoreboard players get #total_tick mgs.data
scoreboard players operation #tick_mod mgs.data %= #6 mgs.data
execute if score #tick_mod mgs.data matches 0 if entity @a[scores={mgs.mp.in_game=1,mgs.special.tracker=1..}] run function mgs:v5.1.0/multiplayer/perks/tracker_tick

function mgs:v5.1.0/shared/maps/call_script_at_base {script:"tick"}

