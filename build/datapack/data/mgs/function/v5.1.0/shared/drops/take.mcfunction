
#> mgs:v5.1.0/shared/drops/take
#
# @executed	at @e[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/shared/drops/collect
#

execute if score #pick_g0 mgs.data matches 0 run item replace entity @s hotbar.1 from entity @n[type=minecraft:item_display,tag=mgs.dropped_gun,distance=..3] contents
execute if score #pick_g0 mgs.data matches 1 run item replace entity @s hotbar.2 from entity @n[type=minecraft:item_display,tag=mgs.dropped_gun,distance=..3] contents
playsound minecraft:entity.item.pickup player @a[distance=..24] ~ ~ ~
kill @n[type=minecraft:item_display,tag=mgs.dropped_gun,distance=..3]
kill @e[tag=bs.interaction.target]

