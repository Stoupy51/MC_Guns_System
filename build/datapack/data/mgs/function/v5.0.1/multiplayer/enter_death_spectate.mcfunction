
#> mgs:v5.0.1/multiplayer/enter_death_spectate
#
# @executed	at @s
#
# @within	mgs:v5.0.1/multiplayer/simulate_death
#			mgs:v5.0.1/multiplayer/on_respawn
#

# S&D: no respawning, mark as dead and go spectator
execute if data storage mgs:multiplayer game{gamemode:"snd"} run return run function mgs:v5.0.1/multiplayer/gamemodes/snd/on_death

# Set player to spectator mode for 3 seconds (60 ticks)
gamemode spectator @s
scoreboard players set @s mgs.mp.spectate_timer 60

# Spectate attacker (if tagged) or random alive player
spectate @p[tag=mgs.temp_killer,gamemode=!spectator] @s
execute unless entity @a[tag=mgs.temp_killer] run function mgs:v5.0.1/multiplayer/spectate_random_player
tag @a[tag=mgs.temp_killer] remove mgs.temp_killer

# Announce death & playsound
title @s title [{"text":"☠","color":"red"}]
title @s subtitle [{"translate":"mgs.respawning_in_3_seconds","color":"gray"}]
execute at @s run playsound minecraft:entity.player.hurt ambient @s

