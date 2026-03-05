
#> mgs:v5.0.0/projectile/set_model
#
# @executed	anchored eyes & positioned ^ ^ ^0.69
#
# @within	mgs:v5.0.0/projectile/init with entity @s data.config
#
# @args		proj_model (unknown)
#

$data modify entity @s item set value {id:"minecraft:paper", count:1, components:{"minecraft:item_model":"mgs:$(proj_model)"}}
data modify entity @s item_display set value "fixed"
data modify entity @s brightness set value {sky: 15, block: 15}

