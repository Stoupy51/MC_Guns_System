
#> mgs:v5.1.0/maps/editor/set_door_link_number
#
# @within	string in mgs:v5.1.0/maps/editor/show_element_config {field:\"price\",value:1000}
#			string in mgs:v5.1.0/maps/editor/show_element_config {field:\"partial_price\",value:0}
#			string in mgs:v5.1.0/maps/editor/show_element_config {field:\"back_group_id\",value:-1}
#			string in mgs:v5.1.0/maps/editor/show_element_config {field:\"animation\",value:0}
#
# @args		field (string)
#			value (int)
#

$data modify storage mgs:temp _door_set set value {field:"$(field)",value:$(value)}
function mgs:v5.1.0/maps/editor/set_door_link_apply

