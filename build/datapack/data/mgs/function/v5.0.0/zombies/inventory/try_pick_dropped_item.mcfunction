
#> mgs:v5.0.0/zombies/inventory/try_pick_dropped_item
#
# @executed	as the player & at current position
#
# @within	mgs:v5.0.0/zombies/inventory/enforce_slot {slot:"$(slot)",expected_nbt:$(expected_nbt)}
#
# @args		slot (string)
#			expected_nbt (compound)
#

$execute if score #zb_inv_found mgs.data matches 0 run item replace entity @p[tag=mgs.inv_slot_owner] $(slot) from entity @n[type=item,distance=..8,nbt={Item:{components:{"minecraft:custom_data":$(expected_nbt)}}}] contents
$execute if score #zb_inv_found mgs.data matches 0 run kill @n[type=item,distance=..8,nbt={Item:{components:{"minecraft:custom_data":$(expected_nbt)}}}]
scoreboard players set #zb_inv_found mgs.data 1

