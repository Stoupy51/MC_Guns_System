
#> mgs:v5.1.0/multiplayer/enter_death_spectate
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/simulate_death
#			mgs:v5.1.0/multiplayer/on_respawn
#

# First, while the gun is still held: it can be picked up for 30 s.
execute at @s run function mgs:v5.1.0/multiplayer/drop_held_weapon

# S&D: no respawn.
execute if data storage mgs:multiplayer game{gamemode:"snd"} run return run function mgs:v5.1.0/multiplayer/gamemodes/snd/on_death

# 3 s of spectating.
gamemode spectator @s
scoreboard players set @s mgs.mp.spectate_timer 60

spectate @p[tag=mgs.temp_killer,gamemode=!spectator] @s
execute unless entity @a[tag=mgs.temp_killer] run function mgs:v5.1.0/multiplayer/spectate_random_player
tag @a[tag=mgs.temp_killer] remove mgs.temp_killer

title @s times 0 70 10
title @s title ["☠"]
title @s subtitle [{"translate":"mgs.respawning_in_3_seconds","color":"gray"}]
execute at @s run playsound minecraft:entity.player.hurt ambient @s

