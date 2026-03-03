
#> mgs:v5.0.0/multiplayer/auto_apply_default
#
# @executed	as @a & at @s
#
# @within	mgs:v5.0.0/multiplayer/start [ as @a & at @s ]
#

# Set mp.class to negative default ID (custom loadout)
scoreboard players operation @s mgs.mp.class = @s mgs.mp.default
scoreboard players operation @s mgs.mp.class *= #minus_one mgs.data

# Apply the loadout
function mgs:v5.0.0/multiplayer/apply_class

