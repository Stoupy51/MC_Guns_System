
#> mgs:v5.0.0/zombies/pap/store_data
#
# @within	mgs:v5.0.0/zombies/pap/setup_iter with storage mgs:temp _pap_store
#
# @args		id (unknown)
#			name (unknown)
#			display_tag (unknown)
#			display_item_id (unknown)
#			display_item_model (unknown)
#

$data modify storage mgs:zombies pap_data."$(id)" set value {name:"$(name)",display_tag:"$(display_tag)",display_item_id:"$(display_item_id)",display_item_model:"$(display_item_model)"}

