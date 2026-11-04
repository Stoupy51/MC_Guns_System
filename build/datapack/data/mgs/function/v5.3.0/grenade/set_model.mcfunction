
#> mgs:v5.3.0/grenade/set_model
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/grenade/init with entity @s data.config
#
# @args		proj_model (unknown)
#

$data modify entity @s item set value {id:"minecraft:paper", count:1, components:{"minecraft:item_model":"mgs:$(proj_model)"}}
data modify entity @s item_display set value "fixed"
data modify entity @s brightness set value {sky: 15, block: 15}
data modify entity @s teleport_duration set value 1

