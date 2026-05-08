
#> mgs:v5.0.1/ammo/inventory/consume_partial
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/ammo/inventory/process_slot {slot:"$(slot)"}
#
# @args		slot (string)
#

# Set the stack count to the remaining bullets (#bullets = remaining items in stack)
$item modify entity @s $(slot) mgs:v5.0.1/set_consumable_count

# Update player's ammo count
scoreboard players operation @s mgs.remaining_bullets = #found_ammo mgs.data

