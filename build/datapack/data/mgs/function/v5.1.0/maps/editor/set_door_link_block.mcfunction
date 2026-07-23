
#> mgs:v5.1.0/maps/editor/set_door_link_block
#
# @within	string in mgs:v5.1.0/maps/editor/show_element_config
#
# @args		block (unknown)
#

$data modify storage mgs:temp _door_set set value {field:"block",value:"$(block)"}
function mgs:v5.1.0/maps/editor/set_door_link_apply

