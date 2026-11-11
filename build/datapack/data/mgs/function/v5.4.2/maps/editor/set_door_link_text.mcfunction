
#> mgs:v5.4.2/maps/editor/set_door_link_text
#
# @within	mgs:v5.4.2/dialog/close_then
#			string in mgs:v5.4.2/maps/editor/show_element_config {field:\"title\",value:\"Door\"}
#			string in mgs:v5.4.2/maps/editor/show_element_config {field:\"back_name\",value:\"Door\"}
#			string in mgs:v5.4.2/maps/editor/show_element_config {field:\"block\",value:\"\"}
#			string in mgs:v5.4.2/maps/editor/show_element_config {field:\"sound\",value:\"\"}
#
# @args		field (string)
#			value (string)
#

$data modify storage mgs:temp _door_set set value {field:"$(field)",value:"$(value)"}
function mgs:v5.4.2/maps/editor/set_door_link_apply

