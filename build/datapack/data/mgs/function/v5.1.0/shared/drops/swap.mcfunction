
#> mgs:v5.1.0/shared/drops/swap
#
# @executed	at @e[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/shared/drops/collect
#

item replace entity B5-0-0-0-3 contents from entity @s hotbar.1
execute if score #pick_sel mgs.data matches 2 run item replace entity B5-0-0-0-3 contents from entity @s hotbar.2
data modify storage mgs:temp _swapw set from entity B5-0-0-0-3 item

# Held guns carry remaining_bullets:-1 in their item NBT (the live count is on the scoreboard), so sync it in
execute store result storage mgs:temp _swapw.components."minecraft:custom_data".mgs.stats.remaining_bullets int 1 run scoreboard players get @s mgs.remaining_bullets

execute if score #pick_sel mgs.data matches 1 run item replace entity @s hotbar.1 from entity @n[type=minecraft:item_display,tag=mgs.dropped_gun,distance=..3] contents
execute if score #pick_sel mgs.data matches 2 run item replace entity @s hotbar.2 from entity @n[type=minecraft:item_display,tag=mgs.dropped_gun,distance=..3] contents
data modify entity @n[type=minecraft:item_display,tag=mgs.dropped_gun,distance=..3] item set from storage mgs:temp _swapw
playsound minecraft:entity.item.pickup player @a[distance=..24] ~ ~ ~
scoreboard players set @n[type=minecraft:item_display,tag=mgs.dropped_gun,distance=..3] mgs.drop_timer 600
scoreboard players set @n[type=minecraft:interaction,tag=mgs.drop_int,distance=..3] mgs.drop_timer 600

## sourceMappingURL=swap.mcfunction.map
