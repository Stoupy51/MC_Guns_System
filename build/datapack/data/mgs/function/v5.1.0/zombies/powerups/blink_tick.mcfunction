
#> mgs:v5.1.0/zombies/powerups/blink_tick
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/powerups/entity_tick
#

execute if score #zb_blink_state mgs.data matches 0 run data modify entity @s Item.components."minecraft:custom_data".mgs.powerup_model set from entity @s Item.components."minecraft:item_model"
execute if score #zb_blink_state mgs.data matches 0 run data modify entity @s Item.components."minecraft:item_model" set value "minecraft:air"
execute if score #zb_blink_state mgs.data matches 1 run data modify entity @s Item.components."minecraft:item_model" set from entity @s Item.components."minecraft:custom_data".mgs.powerup_model
# text_display has no visibility tag, so view_range toggles it.
execute if score #zb_blink_state mgs.data matches 0 as @n[type=minecraft:text_display,tag=mgs.pu_text,distance=..3] run data merge entity @s {view_range:0.0f}
execute if score #zb_blink_state mgs.data matches 1 as @n[type=minecraft:text_display,tag=mgs.pu_text,distance=..3] run data merge entity @s {view_range:64.0f}

