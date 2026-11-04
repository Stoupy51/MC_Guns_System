
#> mgs:v5.3.0/zombies/pap/set_item_name_with_level
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/zombies/pap/apply_to_slot with storage mgs:temp _pap_name_data
#
# @args		slot (unknown)
#			name (unknown)
#			level (unknown)
#			max (unknown)
#

$item modify entity @s $(slot) {"type":"minecraft:set_components","components":{"minecraft:item_name":[{"text":"$(name)","color":"gold","italic":false},{"text":" (PaP $(level)/$(max))","color":"aqua","italic":false}]}}

