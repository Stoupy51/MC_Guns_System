
#> mgs:v5.4.2/zombies/inventory/restore_slot
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/inventory/restore_loop with storage mgs:temp _restore
#
# @args		slot (unknown)
#

$item replace entity @s container.$(slot) from entity @n[type=minecraft:item_display,tag=mgs.inv_restore] contents

