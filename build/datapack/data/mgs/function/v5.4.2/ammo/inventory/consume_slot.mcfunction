
#> mgs:v5.4.2/ammo/inventory/consume_slot
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/ammo/inventory/process_slot {slot:"$(slot)"}
#
# @args		slot (string)
#

$item replace entity @s $(slot) with air

scoreboard players operation @s mgs.remaining_bullets = #found_ammo mgs.data

