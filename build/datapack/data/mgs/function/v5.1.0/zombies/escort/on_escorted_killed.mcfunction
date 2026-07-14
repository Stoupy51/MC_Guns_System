
#> mgs:v5.1.0/zombies/escort/on_escorted_killed
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/on_zombie_dying [ at @s ]
#

tag @s remove mgs.zb_escorted
scoreboard players remove #zb_escort_count mgs.data 1
execute as @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..8] run function mgs:v5.1.0/zombies/escort/discard_trader

