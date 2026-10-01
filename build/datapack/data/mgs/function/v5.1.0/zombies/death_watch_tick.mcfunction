
#> mgs:v5.1.0/zombies/death_watch_tick
#
# @within	mgs:v5.1.0/zombies/game_tick
#

# From the marker passenger to its vehicle, once DeathTime starts.
execute as @e[type=minecraft:marker,tag=mgs.death_watch] at @s on vehicle if data entity @s {DeathTime:1s} run function mgs:v5.1.0/zombies/on_zombie_dying

# Death groan keyed on Health, which is 0 the instant it dies: DeathTime is preset to -16, so the intercept above
# lands 17 ticks late. zb_dying fires it once; dogs are skipped, they die with their own wolf vocals.
execute as @e[type=minecraft:marker,tag=mgs.death_watch] at @s on vehicle if entity @s[tag=mgs.zombie_round,tag=!mgs.zb_dog,tag=!mgs.zb_dying] if data entity @s {Health:0.0f} run function mgs:v5.1.0/zombies/vocals/death

