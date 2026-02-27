
#> mgs:v5.0.0/ammo/inventory/consume_slot
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/ammo/inventory/process_slot {slot:"$(slot)"}
#
# @args		slot (string)
#

# Clear the consumable magazine from the slot
$item replace entity @s $(slot) with air

# Update player's ammo count
scoreboard players operation @s mgs.remaining_bullets = #found_ammo mgs.data

