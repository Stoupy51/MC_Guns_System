
#> mgs:v5.1.0/zombies/inventory/restore_loop
#
# @executed	as @a[distance=..2,gamemode=!spectator,scores={mgs.zb.in_game=1,mgs.zb.downed=0}]
#
# @within	mgs:v5.1.0/zombies/inventory/restore_inventory
#			mgs:v5.1.0/zombies/inventory/restore_loop
#

data modify storage mgs:temp _restore.item set from storage mgs:temp _restore.items[0]
execute store result score #inv_slot mgs.data run data get storage mgs:temp _restore.item.Slot
data remove storage mgs:temp _restore.item.Slot
data modify entity @n[type=minecraft:item_display,tag=mgs.inv_restore] item set from storage mgs:temp _restore.item

# Slot mapping: 0..35 = container.N (hotbar + main inventory), 100..103 = armor, -106 = offhand
execute if score #inv_slot mgs.data matches 0..35 store result storage mgs:temp _restore.slot int 1 run scoreboard players get #inv_slot mgs.data
execute if score #inv_slot mgs.data matches 0..35 run function mgs:v5.1.0/zombies/inventory/restore_slot with storage mgs:temp _restore
execute if score #inv_slot mgs.data matches 100 run item replace entity @s armor.feet from entity @n[type=minecraft:item_display,tag=mgs.inv_restore] contents
execute if score #inv_slot mgs.data matches 101 run item replace entity @s armor.legs from entity @n[type=minecraft:item_display,tag=mgs.inv_restore] contents
execute if score #inv_slot mgs.data matches 102 run item replace entity @s armor.chest from entity @n[type=minecraft:item_display,tag=mgs.inv_restore] contents
execute if score #inv_slot mgs.data matches 103 run item replace entity @s armor.head from entity @n[type=minecraft:item_display,tag=mgs.inv_restore] contents
execute if score #inv_slot mgs.data matches -106 run item replace entity @s weapon.offhand from entity @n[type=minecraft:item_display,tag=mgs.inv_restore] contents

data remove storage mgs:temp _restore.items[0]
execute if data storage mgs:temp _restore.items[0] run function mgs:v5.1.0/zombies/inventory/restore_loop

