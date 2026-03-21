
#> mgs:v5.0.0/zombies/wallbuys/store_data
#
# @within	mgs:v5.0.0/zombies/wallbuys/setup_iter with storage mgs:temp _wb_store
#
# @args		id (unknown)
#			weapon_id (unknown)
#			name (unknown)
#			magazine_id (unknown)
#			item_name (unknown)
#

$data modify storage mgs:zombies wallbuy_data."$(id)" set value {weapon_id:"$(weapon_id)",name:"$(name)",magazine_id:"$(magazine_id)",item_name:$(item_name)}

