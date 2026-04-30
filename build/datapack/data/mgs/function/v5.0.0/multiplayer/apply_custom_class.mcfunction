
#> mgs:v5.0.0/multiplayer/apply_custom_class
#
# @within	mgs:v5.0.0/multiplayer/apply_class
#

# Store target loadout ID (negate to get positive ID)
scoreboard players operation #loadout_id mgs.data = @s mgs.mp.class
scoreboard players operation #loadout_id mgs.data *= #minus_one mgs.data

# Copy loadouts list for search
data modify storage mgs:temp _find_iter set from storage mgs:multiplayer custom_loadouts

# Recursive search by ID (score-based comparison)
execute if data storage mgs:temp _find_iter[0] run function mgs:v5.0.0/multiplayer/apply_custom_found

