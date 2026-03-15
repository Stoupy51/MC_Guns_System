
#> mgs:v5.0.0/maps/editor/set_door_link_back_name
#
# @executed	at @s & as @n[tag=mgs.map_element,distance=..10]
#
# @within	mgs:v5.0.0/maps/editor/show_element_config {back_name:'Door'}"}, "hover_event": {"action": "show_text", "value": "Sets back_name on ALL doors with same link_id"}}, "\u270e", "]"]]
#
# @args		back_name (string)
#

$data modify storage mgs:temp _door_set set value {field:"back_name",value:"$(back_name)"}
function mgs:v5.0.0/maps/editor/set_door_link_apply

