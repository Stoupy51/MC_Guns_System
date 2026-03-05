
#> mgs:v5.0.0/maps/editor/on_place
#
# @executed	as the player & at current position
#
# @within	advancement mgs:v5.0.0/maps/editor/on_place
#

# Revoke advancement immediately so it can trigger again
advancement revoke @s only mgs:v5.0.0/maps/editor/on_place

# Only process if player is in editor mode
execute unless score @s mgs.mp.map_edit matches 1 run return fail

# Find the newly spawned bat entity (tagged by entity_data)
execute as @e[tag=mgs.new_element,limit=1,sort=nearest] at @s run function mgs:v5.0.0/maps/editor/process_element

