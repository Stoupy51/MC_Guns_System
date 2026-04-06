
#> mgs:v5.0.0/zombies/inventory/drop_wrong_slot_item
#
# @executed	as the player & at current position
#
# @within	mgs:v5.0.0/zombies/inventory/enforce_slot {slot:"$(slot)"}
#			mgs:v5.0.0/zombies/inventory/check_slots {slot:"hotbar.5"}
#			mgs:v5.0.0/zombies/inventory/check_slots {slot:"player.cursor"}
#
# @args		slot (string)
#

tag @s add mgs.inv_slot_owner
summon minecraft:item ~ ~ ~ {Item:{id:"minecraft:stone",count:1},Tags:["mgs.inv_new_drop"]}
$execute as @n[type=item,tag=mgs.inv_new_drop,distance=..1] run function mgs:v5.0.0/zombies/inventory/copy_slot_item_to_drop {slot:"$(slot)"}
tag @s remove mgs.inv_slot_owner
$item replace entity @s $(slot) with air

