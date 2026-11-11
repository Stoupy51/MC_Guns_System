
#> mgs:v5.4.2/zombies/pap/set_item_model_from_scope
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/pap/apply_to_slot with storage mgs:temp _pap_scope_model
#			mgs:v5.4.2/zombies/pap/anim/apply_cosmetics_to_display with storage mgs:temp _pap_scope_model
#
# @args		slot (unknown)
#			model (unknown)
#

$item modify entity @s $(slot) {"type":"minecraft:set_components","components":{"minecraft:item_model":"$(model)"}}

