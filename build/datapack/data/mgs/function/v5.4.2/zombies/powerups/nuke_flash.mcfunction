
#> mgs:v5.4.2/zombies/powerups/nuke_flash
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/powerups/activate/nuke [ as @a[scores={mgs.zb.in_game=1}] ]
#

execute at @s anchored eyes run particle minecraft:flash{color:[1.0,1.0,1.0,1.0]} ^ ^ ^0.4 0 0 0 0 1 force @s

