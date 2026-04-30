
#> mgs:v5.0.0/zombies/pap/set_item_model_from_scope
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/apply_to_slot with storage mgs:temp _pap_scope_model
#			mgs:v5.0.0/zombies/pap/anim/apply_cosmetics_to_display with storage mgs:temp _pap_scope_model
#
# @args		slot (unknown)
#			model (unknown)
#

$item modify entity @s $(slot) {"function":"minecraft:set_components","components":{"minecraft:item_model":"$(model)"}}

