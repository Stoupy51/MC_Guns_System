
#> mgs:v5.3.0/maps/editor/handle_zb_configure
#
# @executed	as @n[tag=mgs.new_element] & at @s
#
# @within	mgs:v5.3.0/maps/editor/process_element
#

# Within 10 blocks. A form opens for the editor who placed the egg.
tag @p[tag=mgs.map_editor,distance=..6,sort=nearest] add mgs.ed_form_user
execute at @s as @n[tag=mgs.map_element,distance=..10] run function mgs:v5.3.0/maps/editor/show_element_config
execute at @s unless entity @n[tag=mgs.map_element,distance=..10] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.no_element_found_within_10_blocks","fallback":"No element found within 10 blocks!","color":"red"}]
tag @a remove mgs.ed_form_user

