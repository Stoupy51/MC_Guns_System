
#> mgs:v5.1.0/multiplayer/auto_apply_default
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/start [ at @s ]
#			mgs:v5.1.0/missions/preload_complete [ at @s ]
#

scoreboard players operation @s mgs.mp.class = @s mgs.mp.default
scoreboard players operation @s mgs.mp.class *= #minus_one mgs.data

function mgs:v5.1.0/multiplayer/apply_class

