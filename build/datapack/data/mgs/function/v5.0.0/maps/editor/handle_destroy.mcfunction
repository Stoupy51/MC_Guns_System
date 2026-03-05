
#> mgs:v5.0.0/maps/editor/handle_destroy
#
# @executed	as @n[tag=mgs.new_element] & at @s
#
# @within	mgs:v5.0.0/maps/editor/process_element
#

# Find the nearest map element marker (not a destroy bat, not the bat itself)
# We search from the destroy bat's position
execute positioned as @s as @n[tag=mgs.map_element,distance=..10] run function mgs:v5.0.0/maps/editor/destroy_element
execute positioned as @s unless entity @n[tag=mgs.map_element,distance=..10] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.no_element_found_within_10_blocks","color":"red"}]

