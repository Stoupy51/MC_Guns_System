
#> mgs:v5.1.0/maps/editor/on_place
#
# @executed	as the player & at current position
#
# @within	advancement mgs:v5.1.0/maps/editor/on_place
#

advancement revoke @s only mgs:v5.1.0/maps/editor/on_place

execute unless score @s mgs.mp.map_edit matches 1 run return fail

# The bat the egg spawned (tagged through entity_data).
execute as @n[tag=mgs.new_element] at @s run function mgs:v5.1.0/maps/editor/process_element

