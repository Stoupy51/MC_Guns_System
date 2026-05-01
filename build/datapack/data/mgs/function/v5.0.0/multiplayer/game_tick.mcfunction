
#> mgs:v5.0.0/multiplayer/game_tick
#
# @within	mgs:v5.0.0/tick
#

# Always enforce sidebar display (objective may be removed/recreated by refresh functions)
scoreboard objectives setdisplay sidebar mgs.sidebar

# Spectate Timer (3s respawn cooldown)
execute as @a[scores={mgs.mp.in_game=1,mgs.mp.spectate_timer=1..}] run scoreboard players remove @s mgs.mp.spectate_timer 1
execute as @a[scores={mgs.mp.in_game=1,mgs.mp.spectate_timer=40},gamemode=spectator] run title @s subtitle [{"translate":"mgs.respawning_in_2_seconds","color":"gray"}]
execute as @a[scores={mgs.mp.in_game=1,mgs.mp.spectate_timer=20},gamemode=spectator] run title @s subtitle [{"translate":"mgs.respawning_in_1_second","color":"gray"}]
execute as @a[scores={mgs.mp.in_game=1,mgs.mp.spectate_timer=0},gamemode=spectator] at @s run function mgs:v5.0.0/multiplayer/actual_respawn

# Timer
scoreboard players remove #mp_timer mgs.data 1

# Timer display every second (20 ticks)
execute store result score #tick_mod mgs.data run scoreboard players get #mp_timer mgs.data
scoreboard players operation #tick_mod mgs.data %= #20 mgs.data
execute if score #tick_mod mgs.data matches 0 run function mgs:v5.0.0/multiplayer/timer_display

# Time's up
execute if score #mp_timer mgs.data matches ..0 run function mgs:v5.0.0/multiplayer/time_up

# Boundary enforcement (skip players with respawn protection)
execute if score #mp_has_boundary mgs.data matches 1 as @e[type=player,scores={mgs.mp.in_game=1,mgs.mp.death_count=0},gamemode=!creative,gamemode=!spectator] at @s run function mgs:v5.0.0/multiplayer/check_bounds

# Out-of-bounds check (skip players with respawn protection)
execute as @e[type=player,scores={mgs.mp.in_game=1,mgs.mp.death_count=0},gamemode=!creative,gamemode=!spectator] at @s if entity @e[tag=mgs.oob_point,distance=..5] run function mgs:v5.0.0/multiplayer/oob_kill

# Gamemode tick dispatch
execute if data storage mgs:multiplayer game{gamemode:"ffa"} run function mgs:v5.0.0/multiplayer/gamemodes/ffa/tick
execute if data storage mgs:multiplayer game{gamemode:"tdm"} run function mgs:v5.0.0/multiplayer/gamemodes/tdm/tick
execute if data storage mgs:multiplayer game{gamemode:"dom"} run function mgs:v5.0.0/multiplayer/gamemodes/dom/tick
execute if data storage mgs:multiplayer game{gamemode:"hp"} run function mgs:v5.0.0/multiplayer/gamemodes/hp/tick
execute if data storage mgs:multiplayer game{gamemode:"snd"} run function mgs:v5.0.0/multiplayer/gamemodes/snd/tick

