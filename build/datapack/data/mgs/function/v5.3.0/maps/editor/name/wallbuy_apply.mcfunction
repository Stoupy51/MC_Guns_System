
#> mgs:v5.3.0/maps/editor/name/wallbuy_apply
#
# @within	mgs:v5.3.0/maps/editor/name/wallbuy with storage mgs:temp _ed_name
#
# @args		weapon_id (unknown)
#

$data modify entity @s data.name set value "Wallbuy $(weapon_id)"
data modify entity @s CustomName set from entity @s data.name

