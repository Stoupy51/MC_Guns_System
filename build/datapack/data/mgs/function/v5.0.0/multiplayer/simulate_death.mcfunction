
#> mgs:v5.0.0/multiplayer/simulate_death
#
# @executed	anchored eyes & positioned ^ ^ ^
#
# @within	mgs:v5.0.0/utils/signal_and_damage
#			mgs:v5.0.0/multiplayer/bounds_kill
#			mgs:v5.0.0/multiplayer/oob_kill
#			mgs:v5.0.0/multiplayer/gamemodes/snd/bomb_explodes [ at @e[tag=mgs.snd_bomb] & as @a[distance=..10,gamemode=!creative,scores={mgs.mp.in_game=1..}] ]
#

# Heal to prevent actual death & Increment death stats
effect give @s instant_health 1 100 true
scoreboard players add @s mgs.mp.deaths 1

# Fire damage signal (hit effects, hitmarker, DPS) if this came from a bullet hit
execute if data storage mgs:input with.amount run function #mgs:signals/damage with storage mgs:input with

# Fire kill signal as attacker (if attacker exists in input)
execute if data storage mgs:input with.attacker run function mgs:v5.0.0/multiplayer/simulate_death_fire_kill with storage mgs:input with

# No attacker: random funny self-death message
execute unless data storage mgs:input with.attacker run function mgs:v5.0.0/multiplayer/random_death_message

# Increment death stats
scoreboard players add @s mgs.mp.deaths 1

# S&D: no respawning, mark as dead and go spectator
execute if data storage mgs:multiplayer game{gamemode:"snd"} run return run function mgs:v5.0.0/multiplayer/gamemodes/snd/on_death

# Set player to spectator mode for 3 seconds (60 ticks)
gamemode spectator @s
scoreboard players set @s mgs.mp.spectate_timer 60

# Spectate attacker (tagged by fire_kill) or random
spectate @p[tag=mgs.temp_killer,gamemode=!spectator] @s
execute unless entity @a[tag=mgs.temp_killer] run function mgs:v5.0.0/multiplayer/spectate_random_player
tag @a[tag=mgs.temp_killer] remove mgs.temp_killer

# Announce death & playsound
title @s title [{"text":"☠","color":"red"}]
title @s subtitle [{"translate":"mgs.respawning_in_3_seconds","color":"gray"}]
execute at @s run playsound minecraft:entity.player.hurt ambient @s

