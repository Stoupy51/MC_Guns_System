
#> mgs:v5.0.0/zombies/on_respawn
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# Reset death counter
scoreboard players set @s mgs.mp.death_count 0

# Increment down count
scoreboard players add @s mgs.zb.downs 1

# Set player to spectator mode for 5 seconds (100 ticks) before actual respawn
gamemode spectator @s
scoreboard players set @s mgs.mp.spectate_timer 100

# Spectate a random alive in-game player
function mgs:v5.0.0/zombies/spectate_random_player

# Announce
title @s title [{"text":"\u2620","color":"red"}]
title @s subtitle [{"translate": "mgs.respawning_in_5_seconds","color":"gray"}]

