
#> mgs:v5.4.2/utils/update_model
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zoom/remove with storage mgs:input with
#			mgs:v5.4.2/zoom/set with storage mgs:input with
#
# @args		item_model (string)
#

$item modify entity @s weapon.mainhand {"type": "minecraft:set_components","components": {"minecraft:item_model": "$(item_model)"}}

