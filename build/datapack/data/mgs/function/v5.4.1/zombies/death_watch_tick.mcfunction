
#> mgs:v5.4.1/zombies/death_watch_tick
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/game_tick
#

# From the marker passenger to its vehicle, once DeathTime starts.
execute as @e[type=minecraft:marker,tag=mgs.death_watch] at @s on vehicle if data entity @s {DeathTime:1s} run function mgs:v5.4.1/zombies/on_zombie_dying

# A jockey part at 0 Health takes its mate down now, not 17 ticks later when the intercept above fires.
execute if score #zb_jockey_round mgs.data matches 1 as @e[type=minecraft:marker,tag=mgs.death_watch] on vehicle if entity @s[tag=mgs.zb_jockey,tag=!mgs.zb_jockey_linked] if data entity @s {Health:0.0f} run function mgs:v5.4.1/zombies/jockey/link

# Death groan keyed on Health, which is 0 the instant it dies: DeathTime is preset to -16, so the intercept above
# lands 17 ticks late. zb_dying fires it once; other entities than zombies die with their own vocals.
execute as @e[type=minecraft:marker,tag=mgs.death_watch] at @s on vehicle if entity @s[type=minecraft:zombie,tag=mgs.zombie_round,tag=!mgs.zb_dying] if data entity @s {Health:0.0f} run function mgs:v5.4.1/zombies/vocals/death

