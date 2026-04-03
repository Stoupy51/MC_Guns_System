
#> mgs:v5.0.0/zombies/pap/set_item_name
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/apply_to_slot with storage mgs:temp _pap_apply_name
#
# @args		slot (unknown)
#			name (unknown)
#

$item modify entity @s $(slot) {"function":"minecraft:set_components","components":{"minecraft:item_name":{"text":"$(name)","color":"gold","italic":false}}}

