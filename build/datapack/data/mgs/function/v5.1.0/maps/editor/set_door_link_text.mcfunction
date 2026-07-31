
#> mgs:v5.1.0/maps/editor/set_door_link_text
#
# @within	string in mgs:v5.1.0/maps/editor/show_element_config {field:\"name\",value:\"Door\"}
#			string in mgs:v5.1.0/maps/editor/show_element_config {field:\"back_name\",value:\"Door\"}
#			string in mgs:v5.1.0/maps/editor/show_element_config {field:\"block\",value:\"\"}
#			string in mgs:v5.1.0/maps/editor/show_element_config {field:\"sound\",value:\"\"}
#
# @args		field (string)
#			value (string)
#

$data modify storage mgs:temp _door_set set value {field:"$(field)",value:"$(value)"}
function mgs:v5.1.0/maps/editor/set_door_link_apply

