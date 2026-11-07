
#> mgs:v5.4.0/zombies/pap/set_item_lore
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/pap/apply_to_slot with storage mgs:temp _pap_apply_lore
#
# @args		slot (unknown)
#			lore (unknown)
#

$item modify entity @s $(slot) {"type":"minecraft:set_components","components":{"minecraft:lore":$(lore)}}

