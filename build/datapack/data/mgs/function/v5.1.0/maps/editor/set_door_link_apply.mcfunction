
#> mgs:v5.1.0/maps/editor/set_door_link_apply
#
# @within	mgs:v5.1.0/maps/editor/set_door_link_text
#			mgs:v5.1.0/maps/editor/set_door_link_number
#

execute unless entity @n[tag=mgs.element.door,distance=..10] run return run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_door_found_within_10_blocks","color":"red"}]
execute store result score #link_id mgs.data run data get entity @n[tag=mgs.element.door,distance=..10] data.link_id
execute as @e[tag=mgs.element.door] run function mgs:v5.1.0/maps/editor/door_set_if_match
tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.updated","color":"green"},{"storage":"mgs:temp","nbt":"_door_set.field","color":"yellow"},{"translate":"mgs.for_all_doors_with_matching_link_id","color":"green"}]

