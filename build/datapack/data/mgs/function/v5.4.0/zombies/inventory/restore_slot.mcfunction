
#> mgs:v5.4.0/zombies/inventory/restore_slot
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/inventory/restore_loop with storage mgs:temp _restore
#
# @args		slot (unknown)
#

$item replace entity @s container.$(slot) from entity @n[type=minecraft:item_display,tag=mgs.inv_restore] contents

