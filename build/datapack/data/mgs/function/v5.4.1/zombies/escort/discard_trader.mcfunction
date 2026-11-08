
#> mgs:v5.4.1/zombies/escort/discard_trader
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/game_tick [ at @s ]
#			mgs:v5.4.1/zombies/escort/release [ as @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..8] ]
#			mgs:v5.4.1/zombies/escort/give_up [ as @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..8] ]
#			mgs:v5.4.1/zombies/escort/on_escorted_killed [ as @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..8] ]
#			mgs:v5.4.1/zombies/escort/end_at_trader
#

tp @s ~ ~-1000 ~
kill @s

