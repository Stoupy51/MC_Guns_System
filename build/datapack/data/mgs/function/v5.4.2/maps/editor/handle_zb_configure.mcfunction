
#> mgs:v5.4.2/maps/editor/handle_zb_configure
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/editor/process_element
#

# Within 10 blocks.
execute at @s as @n[tag=mgs.map_element,distance=..10] run function mgs:v5.4.2/maps/editor/show_element_config
execute at @s unless entity @n[tag=mgs.map_element,distance=..10] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.no_element_found_within_10_blocks","fallback":"No element found within 10 blocks!","color":"red"}]

