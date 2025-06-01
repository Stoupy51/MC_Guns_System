
#> mgs:v5.0.0/switch/modify_attack_speed
#
# @within	mgs:v5.0.0/switch/sync_attack_speed_with_cooldown
#

# Copy weapon from player's mainhand slot to item_display entity
item replace entity @s contents from entity @p[tag=mgs.to_modify] weapon.mainhand

# Modify attack speed attribute modifier
execute unless data entity @s item.components."minecraft:attribute_modifiers" run data modify entity @s item.components."minecraft:attribute_modifiers" set value []
execute unless data entity @s item.components."minecraft:attribute_modifiers"[{"type":"minecraft:attack_speed"}] run data modify entity @s item.components."minecraft:attribute_modifiers" append value {"type":"attack_speed","amount":0.0d,"operation":"add_value","slot":"mainhand","id":"minecraft:base_attack_speed"}
execute store result entity @s item.components."minecraft:attribute_modifiers"[{"type":"minecraft:attack_speed"}].amount double 0.001 run scoreboard players get #attack_speed mgs.data

# Modify tooltip display
data modify entity @s item.components."minecraft:tooltip_display" set value {"hide_tooltip":false,"hidden_components":["minecraft:attribute_modifiers"]}

# Copy back weapon to player's mainhand slot
item replace entity @p[tag=mgs.to_modify] weapon.mainhand from entity @s contents

# Kill item_display entity
kill @s

