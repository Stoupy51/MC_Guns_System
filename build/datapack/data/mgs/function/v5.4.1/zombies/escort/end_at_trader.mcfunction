
#> mgs:v5.4.1/zombies/escort/end_at_trader
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/game_tick [ at @s ]
#			mgs:v5.4.1/zombies/barricades/freeze_zombies
#

execute as @e[tag=mgs.zb_escorted,distance=..8,limit=1,sort=nearest] run function mgs:v5.4.1/zombies/escort/detach
function mgs:v5.4.1/zombies/escort/discard_trader

