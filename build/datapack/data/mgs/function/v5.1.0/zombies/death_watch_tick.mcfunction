
#> mgs:v5.1.0/zombies/death_watch_tick
#
# @within	mgs:v5.1.0/zombies/game_tick
#

# Move execution from marker passenger -> vehicle (zombie), then intercept once DeathTime starts.
execute as @e[type=minecraft:marker,tag=mgs.death_watch] at @s on vehicle if data entity @s {DeathTime:1s} run function mgs:v5.1.0/zombies/on_zombie_dying

# Death groan, keyed on Health rather than on the intercept above. Enemies are spawned with DeathTime
# preset to -16 (types/normal, types/dog), so that intercept only lands 17 ticks (0.85s) after the enemy
# actually died — the groan then arrived after the fall animation, which reads as a bug.
# Health is 0 the instant it dies, which is the moment we want. Scaled by 1000 so an enemy on its last
# 0.4 HP cannot truncate to 0 and groan while still alive. zb_dying makes it fire exactly once, since
# Health stays 0 for the whole death animation, and also stops paying for the read afterwards.
# Dogs are skipped: they are not Silent and already die with their own wolf vocals.
execute as @e[type=minecraft:marker,tag=mgs.death_watch] on vehicle if entity @s[tag=mgs.zombie_round,tag=!mgs.zb_dog,tag=!mgs.zb_dying] store result score @s mgs.zb.hp run data get entity @s Health 1000
execute as @e[tag=mgs.zombie_round,tag=!mgs.zb_dog,tag=!mgs.zb_dying,scores={mgs.zb.hp=..0}] at @s run function mgs:v5.1.0/zombies/vocals/death

