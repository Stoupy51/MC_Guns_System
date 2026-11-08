
#> mgs:v5.4.1/multiplayer/apply_slot_count
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/apply_next_slot with storage mgs:temp current_slot
#
# @args		slot (unknown)
#			count (unknown)
#

$item modify entity @s $(slot) {"type":"minecraft:set_count","count":$(count),"add":false}

