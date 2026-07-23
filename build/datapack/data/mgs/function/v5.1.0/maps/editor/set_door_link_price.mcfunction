
#> mgs:v5.1.0/maps/editor/set_door_link_price
#
# @within	string in mgs:v5.1.0/maps/editor/show_element_config
#
# @args		price (unknown)
#

$data modify storage mgs:temp _door_set set value {field:"price",value:$(price)}
function mgs:v5.1.0/maps/editor/set_door_link_apply

