
#> mgs:v5.4.2/zombies/inventory/copy_slot_item_to_drop
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/inventory/drop_wrong_slot_item {slot:"$(slot)"}
#
# @args		slot (string)
#

$item replace entity @s contents from entity @p[tag=mgs.inv_slot_owner] $(slot)
data modify entity @s PickupDelay set value 0s
data modify entity @s Thrower set from entity @p[tag=mgs.inv_slot_owner] UUID
data modify entity @s Owner set from entity @s Thrower
tag @s remove mgs.inv_new_drop

