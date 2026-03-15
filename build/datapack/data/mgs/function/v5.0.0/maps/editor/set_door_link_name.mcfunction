
#> mgs:v5.0.0/maps/editor/set_door_link_name
#
# @executed	at @s & as @n[tag=mgs.map_element,distance=..10]
#
# @within	mgs:v5.0.0/maps/editor/show_element_config {name:'Door'}"}, "hover_event": {"action": "show_text", "value": "Sets name on ALL doors with same link_id"}}, "\u270e", "]"]]
#
# @args		name (string)
#

$data modify storage mgs:temp _door_set set value {field:"name",value:"$(name)"}
function mgs:v5.0.0/maps/editor/set_door_link_apply

