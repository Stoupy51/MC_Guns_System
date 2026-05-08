
#> mgs:v5.0.1/multiplayer/auto_apply_default
#
# @executed	at @s
#
# @within	mgs:v5.0.1/multiplayer/start [ at @s ]
#			mgs:v5.0.1/missions/preload_complete [ at @s ]
#

# Set mp.class to negative default ID (custom loadout)
scoreboard players operation @s mgs.mp.class = @s mgs.mp.default
scoreboard players operation @s mgs.mp.class *= #minus_one mgs.data

# Apply the loadout
function mgs:v5.0.1/multiplayer/apply_class

