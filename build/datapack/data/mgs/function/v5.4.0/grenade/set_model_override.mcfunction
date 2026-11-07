
#> mgs:v5.4.0/grenade/set_model_override
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/grenade/init with entity @s data.config
#
# @args		model_override (unknown)
#

$data modify entity @s item.components."minecraft:item_model" set value "$(model_override)"

