
#> mgs:v5.0.0/multiplayer/apply_slot_loot
#
# @within	mgs:v5.0.0/multiplayer/apply_next_slot with storage mgs:temp current_slot
#
# @args		slot (unknown)
#			loot (unknown)
#

$loot replace entity @s $(slot) loot $(loot)

