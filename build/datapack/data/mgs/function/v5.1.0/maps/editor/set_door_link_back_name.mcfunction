
#> mgs:v5.1.0/maps/editor/set_door_link_back_name
#
# @within	string in mgs:v5.1.0/maps/editor/show_element_config
#
# @args		back_name (unknown)
#

$data modify storage mgs:temp _door_set set value {field:"back_name",value:"$(back_name)"}
function mgs:v5.1.0/maps/editor/set_door_link_apply

