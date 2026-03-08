
#> mgs:v5.0.0/maps/editor/set_door_link_price
#
# @executed	at @s & as @n[tag=mgs.map_element,distance=..10]
#
# @within	mgs:v5.0.0/maps/editor/show_element_config {price:1000}"}, "hover_event": {"action": "show_text", "value": "Sets price on ALL doors with same link_id"}}, "\u270e", "]"]]
#
# @args		price (int)
#

$data modify storage mgs:temp _door_set_price set value $(price)
execute store result score #_link_id mgs.data run data get entity @n[tag=mgs.element.door,distance=..10] data.link_id
execute as @e[tag=mgs.element.door] run function mgs:v5.0.0/maps/editor/door_price_if_match
tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.updated_price_for_all_doors_with_matching_link_id","color":"green"}]

