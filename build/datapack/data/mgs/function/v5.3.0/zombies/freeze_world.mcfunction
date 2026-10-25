
#> mgs:v5.3.0/zombies/freeze_world
#
# @executed	as the player & at current position
#
# @within	mgs:v5.3.0/zombies/freeze_on
#			mgs:v5.3.0/zombies/suspend
#

execute as @e[tag=mgs.zombie_round] unless data entity @s {NoAI:1b} run function mgs:v5.3.0/zombies/freeze_mob
execute as @a[scores={mgs.zb.in_game=1}] run function mgs:v5.3.0/zombies/freeze_player

