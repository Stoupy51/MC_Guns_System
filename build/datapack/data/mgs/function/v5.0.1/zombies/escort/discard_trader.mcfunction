
#> mgs:v5.0.1/zombies/escort/discard_trader
#
# @executed	at @s
#
# @within	mgs:v5.0.1/zombies/game_tick [ at @s ]
#			mgs:v5.0.1/zombies/escort/release [ as @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..8] ]
#			mgs:v5.0.1/zombies/escort/give_up [ as @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..8] ]
#

tp @s ~ ~-1000 ~
kill @s

