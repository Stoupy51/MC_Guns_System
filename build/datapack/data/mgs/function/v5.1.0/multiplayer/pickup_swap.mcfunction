
#> mgs:v5.1.0/multiplayer/pickup_swap
#
# @executed	at @e[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/multiplayer/pickup_collect
#

data modify storage mgs:temp _swapw set from entity @s Inventory[{Slot:0b}]
execute if score #pick_sel mgs.data matches 1 run data modify storage mgs:temp _swapw set from entity @s Inventory[{Slot:1b}]
data remove storage mgs:temp _swapw.Slot

# Held guns carry remaining_bullets:-1 in their item NBT (the live count is on the scoreboard), so sync it in
execute store result storage mgs:temp _swapw.components."minecraft:custom_data".mgs.stats.remaining_bullets int 1 run scoreboard players get @s mgs.remaining_bullets

execute if score #pick_sel mgs.data matches 0 run item replace entity @s hotbar.0 from entity @n[type=minecraft:item_display,tag=mgs.mp_dropped_gun,distance=..3] contents
execute if score #pick_sel mgs.data matches 1 run item replace entity @s hotbar.1 from entity @n[type=minecraft:item_display,tag=mgs.mp_dropped_gun,distance=..3] contents
data modify entity @n[type=minecraft:item_display,tag=mgs.mp_dropped_gun,distance=..3] item set from storage mgs:temp _swapw
playsound minecraft:entity.item.pickup player @a[distance=..24] ~ ~ ~
scoreboard players set @n[type=minecraft:item_display,tag=mgs.mp_dropped_gun,distance=..3] mgs.mp.drop_timer 600
scoreboard players set @n[type=minecraft:interaction,tag=mgs.mp_drop_int,distance=..3] mgs.mp.drop_timer 600

