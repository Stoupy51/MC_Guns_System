
#> mgs:v5.1.0/maps/editor/handle_destroy
#
# @executed	as @n[tag=mgs.new_element] & at @s
#
# @within	mgs:v5.1.0/maps/editor/process_element
#

# Within 3 blocks.
execute at @s unless entity @n[tag=mgs.map_element,distance=..3] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_element_found_within_3_blocks","color":"red"}]
execute at @s as @n[tag=mgs.map_element,distance=..3] run function mgs:v5.1.0/maps/editor/destroy_element

# So a destroyed machine's model disappears at once.
function mgs:v5.1.0/maps/editor/refresh_displays

