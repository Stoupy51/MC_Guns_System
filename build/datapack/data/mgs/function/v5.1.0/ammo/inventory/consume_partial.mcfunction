
#> mgs:v5.1.0/ammo/inventory/consume_partial
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/ammo/inventory/process_slot {slot:"$(slot)"}
#
# @args		slot (string)
#

# #bullets is the items left in the stack.
$item modify entity @s $(slot) mgs:v5.1.0/set_consumable_count

scoreboard players operation @s mgs.remaining_bullets = #found_ammo mgs.data

