
#> mgs:v5.4.2/zombies/escort/release
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/escort/zombie_tick
#			mgs:v5.4.2/zombies/escort/walk_ride
#

execute as @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..8] run function mgs:v5.4.2/zombies/escort/discard_trader
function mgs:v5.4.2/zombies/escort/detach

