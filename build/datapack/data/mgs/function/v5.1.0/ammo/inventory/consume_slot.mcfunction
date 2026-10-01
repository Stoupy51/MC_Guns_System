
#> mgs:v5.1.0/ammo/inventory/consume_slot
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/ammo/inventory/process_slot {slot:"$(slot)"}
#
# @args		slot (string)
#

$item replace entity @s $(slot) with air

scoreboard players operation @s mgs.remaining_bullets = #found_ammo mgs.data

