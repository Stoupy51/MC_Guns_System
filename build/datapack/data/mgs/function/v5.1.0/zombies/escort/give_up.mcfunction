
#> mgs:v5.1.0/zombies/escort/give_up
#
# @executed	as @e[tag=mgs.zb_escorted] & at @s
#
# @within	mgs:v5.1.0/zombies/escort/zombie_tick
#			mgs:v5.1.0/zombies/escort/watchdog
#

tag @s add mgs.zb_escort_failed
execute as @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..8] run function mgs:v5.1.0/zombies/escort/discard_trader
function mgs:v5.1.0/zombies/escort/detach
function mgs:v5.1.0/zombies/on_stuck_zombie

