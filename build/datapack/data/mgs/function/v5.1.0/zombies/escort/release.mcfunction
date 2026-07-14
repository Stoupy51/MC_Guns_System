
#> mgs:v5.1.0/zombies/escort/release
#
# @executed	as @e[tag=mgs.zb_escorted] & at @s
#
# @within	mgs:v5.1.0/zombies/escort/zombie_tick
#

execute as @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..8] run function mgs:v5.1.0/zombies/escort/discard_trader
function mgs:v5.1.0/zombies/escort/detach

