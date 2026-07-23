
#> mgs:v5.1.0/zombies/inventory/restore_inventory
#
# @executed	as @a[distance=..2,gamemode=!spectator,scores={mgs.zb.in_game=1,mgs.zb.downed=0}]
#
# @within	mgs:v5.1.0/zombies/perks/tombstone_collect
#			mgs:v5.1.0/zombies/whos_who/revive_complete
#

clear @s
summon minecraft:item_display ~ ~ ~ {Tags:["mgs.inv_restore","mgs.gm_entity"]}
execute if data storage mgs:temp _restore.items[0] run function mgs:v5.1.0/zombies/inventory/restore_loop
kill @e[type=minecraft:item_display,tag=mgs.inv_restore]
data remove storage mgs:temp _restore

