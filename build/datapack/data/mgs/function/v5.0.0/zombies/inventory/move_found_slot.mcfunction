
#> mgs:v5.0.0/zombies/inventory/move_found_slot
#
# @executed	as the player & at current position
#
# @within	mgs:v5.0.0/zombies/inventory/enforce_slot {from:"hotbar.0",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"hotbar.1",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"hotbar.2",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"hotbar.3",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"hotbar.4",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"hotbar.5",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"hotbar.6",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"hotbar.7",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"hotbar.8",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"weapon.offhand",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.0",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.1",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.2",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.3",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.4",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.5",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.6",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.7",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.8",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.9",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.10",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.11",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.12",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.13",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.14",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.15",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.16",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.17",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.18",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.19",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.20",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.21",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.22",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.23",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.24",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.25",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"inventory.26",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"player.cursor",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"player.crafting.0",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"player.crafting.1",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"player.crafting.2",to:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/enforce_slot {from:"player.crafting.3",to:"$(slot)"}
#
# @args		from (string)
#			to (string)
#

# Swap source and target via temp item_display (handles empty target too)
tag @s add mgs.inv_swapping
$execute summon item_display run function mgs:v5.0.0/zombies/inventory/swap_slots {from:"$(from)",to:"$(to)"}
tag @s remove mgs.inv_swapping
scoreboard players set #zb_inv_found mgs.data 1

