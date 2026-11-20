
#> mgs:v5.4.3/utils/update_model
#
# @within	mgs:v5.4.3/dialog/close_then
#			mgs:v5.4.3/zoom/remove with storage mgs:input with
#			mgs:v5.4.3/zoom/set with storage mgs:input with
#
# @args		item_model (string)
#

$item modify entity @s weapon.mainhand {"type": "minecraft:set_components","components": {"minecraft:item_model": "$(item_model)"}}

