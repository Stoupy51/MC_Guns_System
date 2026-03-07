
#> mgs:v5.0.0/multiplayer/on_respawn
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# Reset death counter
scoreboard players set @s mgs.mp.death_count 0

# Increment death stats
scoreboard players add @s mgs.mp.deaths 1

# Death message: try to find attacker, otherwise random message
tag @s add mgs.temp_victim
execute on attacker run tag @s add mgs.temp_killer
execute if entity @a[tag=mgs.temp_killer] run function mgs:v5.0.0/multiplayer/random_kill_message
execute unless entity @a[tag=mgs.temp_killer] run function mgs:v5.0.0/multiplayer/random_death_message
tag @s remove mgs.temp_victim

# S&D: no respawning, mark as dead and go spectator
execute if data storage mgs:multiplayer game{gamemode:"snd"} run return run function mgs:v5.0.0/multiplayer/gamemodes/snd/on_death

# Set player to spectator mode for 3 seconds (60 ticks) before actual respawn
gamemode spectator @s
scoreboard players set @s mgs.mp.spectate_timer 60

# Try to spectate the player who killed us (last attacker)
execute if entity @a[tag=mgs.temp_killer,gamemode=!spectator] run spectate @p[tag=mgs.temp_killer,gamemode=!spectator] @s

# If no killer found (environmental death), spectate a random alive in-game player
execute unless entity @a[tag=mgs.temp_killer] run function mgs:v5.0.0/multiplayer/spectate_random_player

# Clean up killer tag
tag @a[tag=mgs.temp_killer] remove mgs.temp_killer

# Announce
title @s title [{"text":"☠","color":"red"}]
title @s subtitle [{"translate": "mgs.respawning_in_3_seconds","color":"gray"}]

