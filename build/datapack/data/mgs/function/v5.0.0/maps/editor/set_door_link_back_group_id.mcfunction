
#> mgs:v5.0.0/maps/editor/set_door_link_back_group_id
#
# @executed	at @s & as @n[tag=mgs.map_element,distance=..10]
#
# @within	mgs:v5.0.0/maps/editor/show_element_config {back_group_id:-1}"}, "hover_event": {"action": "show_text", "value": "Sets back_group_id on ALL doors with same link_id"}}, "\u270e", "]"]]
#
# @args		back_group_id (int)
#

$data modify storage mgs:temp _door_set set value {field:"back_group_id",value:$(back_group_id)}
function mgs:v5.0.0/maps/editor/set_door_link_apply

