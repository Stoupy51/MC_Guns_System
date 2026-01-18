
#> mgs:v5.0.0/utils/update_model
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/zoom/remove with storage mgs:input with
#			mgs:v5.0.0/zoom/set with storage mgs:input with
#
# @args		item_model (string)
#

$item modify entity @s weapon.mainhand {"function": "minecraft:set_components","components": {"minecraft:item_model": "$(item_model)"}}

