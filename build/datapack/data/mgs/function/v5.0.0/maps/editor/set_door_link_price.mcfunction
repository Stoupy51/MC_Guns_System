
#> mgs:v5.0.0/maps/editor/set_door_link_price
#
# @executed	at @s & as @n[tag=mgs.map_element,distance=..10]
#
# @within	mgs:v5.0.0/maps/editor/show_element_config {price:1000}"}, "hover_event": {"action": "show_text", "value": "Sets price on ALL doors with same link_id"}}, "\u270e", "]"]]
#
# @args		price (int)
#

$data modify storage mgs:temp _door_set set value {field:"price",value:$(price)}
function mgs:v5.0.0/maps/editor/set_door_link_apply

