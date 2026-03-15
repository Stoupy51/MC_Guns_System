
#> mgs:v5.0.0/maps/editor/set_door_link_sound
#
# @executed	at @s & as @n[tag=mgs.map_element,distance=..10]
#
# @within	mgs:v5.0.0/maps/editor/show_element_config {sound:''}"}, "hover_event": {"action": "show_text", "value": "Sets sound on ALL doors with same link_id"}}, "\u270e", "]"]]
#
# @args		sound (string)
#

$data modify storage mgs:temp _door_set set value {field:"sound",value:"$(sound)"}
function mgs:v5.0.0/maps/editor/set_door_link_apply

