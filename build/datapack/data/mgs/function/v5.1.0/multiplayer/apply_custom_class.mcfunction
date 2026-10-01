
#> mgs:v5.1.0/multiplayer/apply_custom_class
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/apply_class
#

# mp.class is minus the loadout id.
scoreboard players operation #loadout_id mgs.data = @s mgs.mp.class
scoreboard players operation #loadout_id mgs.data *= #minus_one mgs.data

data modify storage mgs:temp _find_iter set from storage mgs:multiplayer custom_loadouts

execute if data storage mgs:temp _find_iter[0] run function mgs:v5.1.0/multiplayer/apply_custom_found

