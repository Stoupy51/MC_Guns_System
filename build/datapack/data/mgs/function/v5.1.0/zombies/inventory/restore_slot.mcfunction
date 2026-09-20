
#> mgs:v5.1.0/zombies/inventory/restore_slot
#
# @executed	as @a[distance=..2,gamemode=!spectator,scores={mgs.zb.in_game=1,mgs.zb.downed=0}]
#
# @within	mgs:v5.1.0/zombies/inventory/restore_loop with storage mgs:temp _restore
#
# @args		slot (unknown)
#

$item replace entity @s container.$(slot) from entity @n[type=minecraft:item_display,tag=mgs.inv_restore] contents

