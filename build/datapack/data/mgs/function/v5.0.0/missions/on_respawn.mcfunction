
#> mgs:v5.0.0/missions/on_respawn
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# Reset death counter & Increment mission death stats
scoreboard players set @s mgs.mp.death_count 0
scoreboard players add @s mgs.mi.deaths 1

# Set player to spectator mode for 3 seconds (60 ticks) before actual respawn
gamemode spectator @s
scoreboard players set @s mgs.mp.spectate_timer 60

# Spectate a random alive in-game player
function mgs:v5.0.0/missions/spectate_random_player

# Announce respawn delay to the dying player
title @s title [{"text":"☠","color":"red"}]
title @s subtitle [{"translate": "mgs.respawning_in_3_seconds","color":"gray"}]

