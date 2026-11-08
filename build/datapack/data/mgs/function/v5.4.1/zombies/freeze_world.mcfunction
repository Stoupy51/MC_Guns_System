
#> mgs:v5.4.1/zombies/freeze_world
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/freeze_on
#			mgs:v5.4.1/zombies/suspend
#

execute as @e[tag=mgs.zombie_round] unless data entity @s {NoAI:1b} run function mgs:v5.4.1/zombies/freeze_mob
execute as @a[scores={mgs.zb.in_game=1}] run function mgs:v5.4.1/zombies/freeze_player

