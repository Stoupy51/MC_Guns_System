
#> mgs:v5.1.0/zombies/vocals/death
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/death_watch_tick [ at @s ]
#

# Health stays 0 for the whole death animation, so this tag is what makes the groan fire exactly once.
# It also drops this zombie out of the Health read in death_watch_tick for the rest of its existence.
tag @s add mgs.zb_dying

execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator,distance=..32] unless score @s mgs.zb.vox_death > #total_tick mgs.data run function mgs:v5.1.0/zombies/vocals/death_for

