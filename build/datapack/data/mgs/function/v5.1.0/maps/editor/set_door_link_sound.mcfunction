
#> mgs:v5.1.0/maps/editor/set_door_link_sound
#
# @within	string in mgs:v5.1.0/maps/editor/show_element_config
#
# @args		sound (unknown)
#

$data modify storage mgs:temp _door_set set value {field:"sound",value:"$(sound)"}
function mgs:v5.1.0/maps/editor/set_door_link_apply

