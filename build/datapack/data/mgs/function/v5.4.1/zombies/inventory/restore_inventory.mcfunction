
#> mgs:v5.4.1/zombies/inventory/restore_inventory
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/perks/tombstone_collect
#			mgs:v5.4.1/zombies/whos_who/revive_complete
#

clear @s
summon minecraft:item_display ~ ~ ~ {Tags:["mgs.inv_restore","mgs.zombies_entity"]}
execute if data storage mgs:temp _restore.items[0] run function mgs:v5.4.1/zombies/inventory/restore_loop
kill @e[type=minecraft:item_display,tag=mgs.inv_restore]
data remove storage mgs:temp _restore

