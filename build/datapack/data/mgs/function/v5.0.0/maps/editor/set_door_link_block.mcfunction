
#> mgs:v5.0.0/maps/editor/set_door_link_block
#
# @executed	at @s & as @n[tag=mgs.map_element,distance=..10]
#
# @within	mgs:v5.0.0/maps/editor/show_element_config {block:\"\"}"}, "hover_event": {"action": "show_text", "value": "Sets block on ALL doors with same link_id"}}, "\u270e", "]"]]
#
# @args		block (unknown)
#

$data modify storage mgs:temp _door_set set value {field:"block",value:"$(block)"}
function mgs:v5.0.0/maps/editor/set_door_link_apply

