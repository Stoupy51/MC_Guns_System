
#> mgs:v5.0.0/maps/editor/door_set_if_match
#
# @executed	as @e[tag=mgs.element.door]
#
# @within	mgs:v5.0.0/maps/editor/set_door_link_apply [ as @e[tag=mgs.element.door] ]
#

execute store result score #check mgs.data run data get entity @s data.link_id
execute if score #check mgs.data = #link_id mgs.data run function mgs:v5.0.0/maps/editor/door_apply_field with storage mgs:temp _door_set

