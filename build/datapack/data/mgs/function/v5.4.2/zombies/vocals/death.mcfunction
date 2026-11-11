
#> mgs:v5.4.2/zombies/vocals/death
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/death_watch_tick [ at @s ]
#

# Health stays 0 for the whole death animation, so this tag makes the groan fire once.
tag @s add mgs.zb_dying

execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator,distance=..32] unless score @s mgs.zb.vox_death > #total_tick mgs.data run function mgs:v5.4.2/zombies/vocals/death_for

