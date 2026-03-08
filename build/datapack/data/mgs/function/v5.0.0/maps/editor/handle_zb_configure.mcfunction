
#> mgs:v5.0.0/maps/editor/handle_zb_configure
#
# @executed	as @n[tag=mgs.new_element] & at @s
#
# @within	mgs:v5.0.0/maps/editor/process_element
#

# Find the nearest map element marker (within 10 blocks)
execute at @s as @n[tag=mgs.map_element,distance=..10] run function mgs:v5.0.0/maps/editor/show_element_config
execute at @s unless entity @n[tag=mgs.map_element,distance=..10] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.no_element_found_within_10_blocks","color":"red"}]

