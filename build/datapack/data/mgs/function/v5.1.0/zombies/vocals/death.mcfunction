
#> mgs:v5.1.0/zombies/vocals/death
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/on_zombie_dying
#

execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator,distance=..32] unless score @s mgs.zb.vox_death > #total_tick mgs.data run function mgs:v5.1.0/zombies/vocals/death_for

