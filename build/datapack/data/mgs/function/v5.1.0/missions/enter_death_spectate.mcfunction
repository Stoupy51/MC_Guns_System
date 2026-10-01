
#> mgs:v5.1.0/missions/enter_death_spectate
#
# @executed	at @s
#
# @within	mgs:v5.1.0/missions/simulate_death
#			mgs:v5.1.0/missions/on_respawn
#

# First, while the gun is still held: it can be picked up for 30 s.
execute at @s run function mgs:v5.1.0/multiplayer/drop_held_weapon

# 3 s of spectating before the respawn.
gamemode spectator @s
scoreboard players set @s mgs.mp.spectate_timer 60

# A simulated death keeps the camera at the death point; a vanilla death already moved the player, so they spectate a teammate.
execute unless score @s mgs.mi.died_here matches 1 run function mgs:v5.1.0/missions/spectate_random_player

title @s times 0 70 10
title @s title ["☠"]
title @s subtitle [{"translate":"mgs.respawning_in_3_seconds","color":"gray"}]
execute at @s run playsound minecraft:entity.player.hurt ambient @s

