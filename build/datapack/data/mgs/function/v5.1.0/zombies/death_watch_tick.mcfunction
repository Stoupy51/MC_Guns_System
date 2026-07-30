
#> mgs:v5.1.0/zombies/death_watch_tick
#
# @within	mgs:v5.1.0/zombies/game_tick
#

# Move execution from marker passenger -> vehicle (enemy) and cache DeathTime.
execute as @e[type=minecraft:marker,tag=mgs.death_watch] on vehicle store result score @s mgs.zb.death_time run data get entity @s DeathTime

# Death groan on the first tick after death. Firing it from the intercept below instead put it 17 ticks
# (0.85s) late — after the fall animation — which reads as a bug rather than as a death.
# Dogs are skipped: they are not Silent and already die with their own wolf vocals.
execute as @e[tag=mgs.zombie_round,tag=!mgs.zb_dog,scores={mgs.zb.death_time=-15}] at @s run function mgs:v5.1.0/zombies/vocals/death

# The removal intercept keeps running from the MARKER, at the marker's position: on_zombie_dying kills
# its own marker with distance=..1, and a zombie's passenger attachment sits ~1.5 blocks up, so
# re-rooting it on the enemy would silently orphan every marker.
execute as @e[type=minecraft:marker,tag=mgs.death_watch] at @s on vehicle if score @s mgs.zb.death_time matches 1 run function mgs:v5.1.0/zombies/on_zombie_dying

