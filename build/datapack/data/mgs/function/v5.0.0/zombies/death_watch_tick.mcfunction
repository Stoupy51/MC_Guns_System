
#> mgs:v5.0.0/zombies/death_watch_tick
#
# @within	mgs:v5.0.0/zombies/game_tick
#

# Move execution from marker passenger -> vehicle (zombie), then intercept once DeathTime starts.
execute as @e[type=minecraft:marker,tag=mgs.death_watch] at @s on vehicle if data entity @s {DeathTime:1s} run function mgs:v5.0.0/zombies/on_zombie_dying

