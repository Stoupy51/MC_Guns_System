
#> mgs:v5.1.0/switch/modify_attack_speed
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/switch/sync_attack_speed_with_cooldown
#

item replace entity @s contents from entity @p[tag=mgs.to_modify] weapon.mainhand

execute unless data entity @s item.components."minecraft:attribute_modifiers" run data modify entity @s item.components."minecraft:attribute_modifiers" set value []
execute unless data entity @s item.components."minecraft:attribute_modifiers"[{"type":"minecraft:attack_speed"}] run data modify entity @s item.components."minecraft:attribute_modifiers" append value {"type":"attack_speed","amount":0.0d,"operation":"add_value","slot":"mainhand","id":"minecraft:base_attack_speed"}
execute store result entity @s item.components."minecraft:attribute_modifiers"[{"type":"minecraft:attack_speed"}].amount double 0.001 run scoreboard players get #attack_speed mgs.data

# Enchantments stay hidden: this overwrites the whole component, and the item hides its empty-named mgs:left_click enchantment.
data modify entity @s item.components."minecraft:tooltip_display" set value {"hide_tooltip":false,"hidden_components":["minecraft:attribute_modifiers","minecraft:enchantments"]}

item replace entity @p[tag=mgs.to_modify] weapon.mainhand from entity @s contents

kill @s

