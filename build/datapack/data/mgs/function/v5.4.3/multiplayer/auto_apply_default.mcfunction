
#> mgs:v5.4.3/multiplayer/auto_apply_default
#
# @within	mgs:v5.4.3/dialog/close_then
#			mgs:v5.4.3/multiplayer/start [ at @s ]
#			mgs:v5.4.3/missions/preload_complete [ at @s ]
#

scoreboard players operation @s mgs.mp.class = @s mgs.mp.default
scoreboard players operation @s mgs.mp.class *= #minus_one mgs.data

function mgs:v5.4.3/multiplayer/apply_class

