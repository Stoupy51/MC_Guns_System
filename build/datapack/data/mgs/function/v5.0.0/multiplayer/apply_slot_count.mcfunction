
#> mgs:v5.0.0/multiplayer/apply_slot_count
#
# @within	mgs:v5.0.0/multiplayer/apply_next_slot with storage mgs:temp current_slot
#
# @args		slot (unknown)
#			count (unknown)
#

$item modify entity @s $(slot) {"function":"minecraft:set_count","count":$(count),"add":false}

