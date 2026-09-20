
#> mgs:v5.1.0/zombies/death_watch_tick
#
# @within	mgs:v5.1.0/zombies/game_tick
#

# Move execution from marker passenger -> vehicle (zombie), then intercept once DeathTime starts.
execute as @e[type=minecraft:marker,tag=mgs.death_watch] at @s on vehicle if data entity @s {DeathTime:1s} run function mgs:v5.1.0/zombies/on_zombie_dying

# Death groan, keyed on Health rather than on the intercept above. Enemies are spawned with DeathTime
# preset to -16 (types/normal, types/dog), so that intercept only lands 17 ticks (0.85s) after the enemy
# actually died — the groan then arrived after the fall animation, which reads as a bug.
# Health is exactly 0.0f the instant it dies (setHealth clamps to 0), which is the moment we want.
# Deliberately the SAME shape as the line above rather than a score cache plus a second @e sweep: that
# line is proven to work in game, and matching NBT costs no more than reading it.
# zb_dying makes it fire exactly once, since Health stays 0 for the whole death animation.
# Dogs are skipped: they are not Silent and already die with their own wolf vocals.
execute as @e[type=minecraft:marker,tag=mgs.death_watch] at @s on vehicle if entity @s[tag=mgs.zombie_round,tag=!mgs.zb_dog,tag=!mgs.zb_dying] if data entity @s {Health:0.0f} run function mgs:v5.1.0/zombies/vocals/death

