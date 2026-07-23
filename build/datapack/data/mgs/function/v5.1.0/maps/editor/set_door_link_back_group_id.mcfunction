
#> mgs:v5.1.0/maps/editor/set_door_link_back_group_id
#
# @within	string in mgs:v5.1.0/maps/editor/show_element_config
#
# @args		back_group_id (unknown)
#

$data modify storage mgs:temp _door_set set value {field:"back_group_id",value:$(back_group_id)}
function mgs:v5.1.0/maps/editor/set_door_link_apply

