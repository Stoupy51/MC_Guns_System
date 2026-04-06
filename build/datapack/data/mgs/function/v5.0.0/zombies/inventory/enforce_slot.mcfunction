
#> mgs:v5.0.0/zombies/inventory/enforce_slot
#
# @executed	as the player & at current position
#
# @within	mgs:v5.0.0/zombies/inventory/check_slots {slot:"hotbar.8",match:"*[custom_data~{mgs:{zb_info:true,zombies:{hotbar:8}}}]",expected_nbt:{mgs:{zb_info:true,zombies:{hotbar:8}}}}
#			mgs:v5.0.0/zombies/inventory/check_slots {slot:"hotbar.7",match:"*[custom_data~{mgs:{gun:true,zombies:{hotbar:7}}}]",expected_nbt:{mgs:{gun:true,zombies:{hotbar:7}}}}
#			mgs:v5.0.0/zombies/inventory/check_slots {slot:"hotbar.6",match:"*[custom_data~{mgs:{gun:true,zombies:{hotbar:6}}}]",expected_nbt:{mgs:{gun:true,zombies:{hotbar:6}}}}
#			mgs:v5.0.0/zombies/inventory/check_slots {slot:"hotbar.2",match:"*[custom_data~{mgs:{gun:true,zombies:{hotbar:2}}}]",expected_nbt:{mgs:{gun:true,zombies:{hotbar:2}}}}
#			mgs:v5.0.0/zombies/inventory/check_slots {slot:"hotbar.1",match:"*[custom_data~{mgs:{gun:true,zombies:{hotbar:1}}}]",expected_nbt:{mgs:{gun:true,zombies:{hotbar:1}}}}
#			mgs:v5.0.0/zombies/inventory/check_slots {slot:"hotbar.0",match:"*[custom_data~{mgs:{knife:true,zombies:{hotbar:0}}}]",expected_nbt:{mgs:{knife:true,zombies:{hotbar:0}}}}
#			mgs:v5.0.0/zombies/inventory/check_slots {slot:"inventory.1",match:"*[custom_data~{mgs:{magazine:true,zombies:{inventory:1}}}]",expected_nbt:{mgs:{magazine:true,zombies:{inventory:1}}}}
#			mgs:v5.0.0/zombies/inventory/check_slots {slot:"inventory.2",match:"*[custom_data~{mgs:{magazine:true,zombies:{inventory:2}}}]",expected_nbt:{mgs:{magazine:true,zombies:{inventory:2}}}}
#			mgs:v5.0.0/zombies/inventory/check_slots {slot:"hotbar.3",match:"*[custom_data~{mgs:{gun:true,zombies:{hotbar:3}}}]",expected_nbt:{mgs:{gun:true,zombies:{hotbar:3}}}}
#			mgs:v5.0.0/zombies/inventory/check_slots {slot:"inventory.3",match:"*[custom_data~{mgs:{magazine:true,zombies:{inventory:3}}}]",expected_nbt:{mgs:{magazine:true,zombies:{inventory:3}}}}
#			mgs:v5.0.0/zombies/inventory/check_slots {slot:"hotbar.4",match:"*[custom_data~{mgs:{zb_ability_item:true,zombies:{hotbar:4}}}]",expected_nbt:{mgs:{zb_ability_item:true,zombies:{hotbar:4}}}}
#
# @args		slot (string)
#			match (string)
#			expected_nbt (compound)
#

$execute if items entity @s $(slot) $(match) run return 1

# Scan all inventory slots for the correct item and swap it into place
scoreboard players set #zb_inv_found mgs.data 0
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s hotbar.0 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"hotbar.0",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s hotbar.1 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"hotbar.1",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s hotbar.2 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"hotbar.2",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s hotbar.3 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"hotbar.3",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s hotbar.4 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"hotbar.4",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s hotbar.5 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"hotbar.5",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s hotbar.6 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"hotbar.6",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s hotbar.7 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"hotbar.7",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s hotbar.8 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"hotbar.8",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s weapon.offhand $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"weapon.offhand",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.0 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.0",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.1 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.1",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.2 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.2",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.3 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.3",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.4 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.4",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.5 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.5",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.6 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.6",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.7 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.7",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.8 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.8",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.9 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.9",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.10 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.10",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.11 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.11",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.12 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.12",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.13 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.13",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.14 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.14",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.15 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.15",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.16 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.16",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.17 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.17",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.18 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.18",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.19 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.19",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.20 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.20",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.21 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.21",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.22 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.22",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.23 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.23",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.24 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.24",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.25 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.25",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s inventory.26 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"inventory.26",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s player.cursor $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"player.cursor",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s player.crafting.0 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"player.crafting.0",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s player.crafting.1 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"player.crafting.1",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s player.crafting.2 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"player.crafting.2",to:"$(slot)"}
$execute if score #zb_inv_found mgs.data matches 0 if items entity @s player.crafting.3 $(match) run function mgs:v5.0.0/zombies/inventory/move_found_slot {from:"player.crafting.3",to:"$(slot)"}

execute if score #zb_inv_found mgs.data matches 1 run return 1

# Not found in any slot: drop wrong zombies item from target slot if present, then try ground pickup
$execute if items entity @s $(slot) *[custom_data~{mgs:{zombies:{}}}] run function mgs:v5.0.0/zombies/inventory/drop_wrong_slot_item {slot:"$(slot)"}

tag @s add mgs.inv_slot_owner
$execute as @e[type=item,distance=..8,nbt={Item:{components:{"minecraft:custom_data":$(expected_nbt)}}}] on origin if entity @s[tag=mgs.inv_slot_owner] run function mgs:v5.0.0/zombies/inventory/try_pick_dropped_item {slot:"$(slot)",expected_nbt:$(expected_nbt)}
tag @s remove mgs.inv_slot_owner

return 0

