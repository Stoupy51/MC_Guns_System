
#> mgs:v5.1.0/zombies/powerups/blink_tick
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.1.0/zombies/powerups/entity_tick
#

# "Off" frame: hide the item entity and the text_display
execute if score #zb_blink_state mgs.data matches 0 run data modify entity @s Item.components."minecraft:custom_data".mgs.powerup_model set from entity @s Item.components."minecraft:item_model"
execute if score #zb_blink_state mgs.data matches 0 run data modify entity @s Item.components."minecraft:item_model" set value "minecraft:air"
# "On" frame: show the item entity again
execute if score #zb_blink_state mgs.data matches 1 run data modify entity @s Item.components."minecraft:item_model" set from entity @s Item.components."minecraft:custom_data".mgs.powerup_model
# text_display has no generic visibility tag — use view_range toggle instead
execute if score #zb_blink_state mgs.data matches 0 as @n[tag=mgs.pu_text,distance=..3] run data merge entity @s {view_range:0.0f}
execute if score #zb_blink_state mgs.data matches 1 as @n[tag=mgs.pu_text,distance=..3] run data merge entity @s {view_range:64.0f}

