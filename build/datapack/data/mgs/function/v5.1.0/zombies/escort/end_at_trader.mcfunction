
#> mgs:v5.1.0/zombies/escort/end_at_trader
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/escort/discard_near_player
#			mgs:v5.1.0/zombies/barriers/freeze_zombies
#

execute as @e[tag=mgs.zb_escorted,distance=..8,limit=1,sort=nearest] run function mgs:v5.1.0/zombies/escort/detach
function mgs:v5.1.0/zombies/escort/discard_trader

