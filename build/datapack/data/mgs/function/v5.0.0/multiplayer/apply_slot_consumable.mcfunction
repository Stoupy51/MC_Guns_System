
#> mgs:v5.0.0/multiplayer/apply_slot_consumable
#
# @within	mgs:v5.0.0/multiplayer/apply_next_slot with storage mgs:temp current_slot
#
# @args		bullets (unknown)
#			slot (unknown)
#

$scoreboard players set #bullets mgs.data $(bullets)
$item modify entity @s $(slot) mgs:v5.0.0/set_consumable_count

