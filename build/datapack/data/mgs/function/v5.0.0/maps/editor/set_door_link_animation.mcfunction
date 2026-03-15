
#> mgs:v5.0.0/maps/editor/set_door_link_animation
#
# @executed	at @s & as @n[tag=mgs.map_element,distance=..10]
#
# @within	mgs:v5.0.0/maps/editor/show_element_config {animation:0}"}, "hover_event": {"action": "show_text", "value": "Sets animation on ALL doors with same link_id"}}, "\u270e", "]"]]
#
# @args		animation (int)
#

$data modify storage mgs:temp _door_set set value {field:"animation",value:$(animation)}
function mgs:v5.0.0/maps/editor/set_door_link_apply

