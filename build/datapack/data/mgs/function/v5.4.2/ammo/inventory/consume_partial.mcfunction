
#> mgs:v5.4.2/ammo/inventory/consume_partial
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/ammo/inventory/process_slot {slot:"$(slot)"}
#
# @args		slot (string)
#

# #bullets is the items left in the stack.
$item modify entity @s $(slot) mgs:v5.4.2/set_consumable_count

scoreboard players operation @s mgs.remaining_bullets = #found_ammo mgs.data

