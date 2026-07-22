
#> mgs:v5.1.0/missions/enter_death_spectate
#
# @executed	at @s
#
# @within	mgs:v5.1.0/missions/simulate_death
#			mgs:v5.1.0/missions/on_respawn
#

# Drop the held gun on the ground (pickable for 30s) before anything else, while still holding it
execute at @s run function mgs:v5.1.0/multiplayer/drop_held_weapon

# Set player to spectator mode for 3 seconds (60 ticks) before actual respawn
gamemode spectator @s
scoreboard players set @s mgs.mp.spectate_timer 60

# Simulated death: the camera is already at the death point, leave it there. A vanilla death has
# teleported the player to the world spawn by now, so those fall back to spectating a teammate.
execute unless score @s mgs.mi.died_here matches 1 run function mgs:v5.1.0/missions/spectate_random_player

# Announce respawn delay to the dying player
title @s title ["☠"]
title @s subtitle [{"translate":"mgs.respawning_in_3_seconds","color":"gray"}]
execute at @s run playsound minecraft:entity.player.hurt ambient @s

