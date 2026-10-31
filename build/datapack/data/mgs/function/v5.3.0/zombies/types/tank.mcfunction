
#> mgs:v5.3.0/zombies/types/tank
#
# @executed	as @n[tag=mgs.zb_new]
#
# @within	mgs:v5.3.0/zombies/types/apply
#

tag @s add mgs.zb_tank

# 75% of the round's speed; the escort taxi reads this base value.
execute store result storage mgs:temp _zb_speed.value double 0.00075 run attribute @s minecraft:movement_speed base get 1000
function mgs:v5.3.0/zombies/set_speed with storage mgs:temp _zb_speed
execute store result score #zb_speed mgs.data run attribute @s minecraft:movement_speed base get 1000
execute if score #zb_speed mgs.data matches 290.. run tag @s add mgs.zb_sprint
execute if score #zb_speed mgs.data matches ..289 run tag @s remove mgs.zb_sprint

# 300% of the health the round just gave (#zb_hp).
scoreboard players operation #zb_hp mgs.data *= #300 mgs.data
scoreboard players operation #zb_hp mgs.data /= #100 mgs.data
execute if score #zb_hp mgs.data matches 3073.. run scoreboard players set #zb_hp mgs.data 3072
function mgs:v5.3.0/zombies/apply_zombie_hp

attribute @s minecraft:scale base set 1.25
item replace entity @s armor.head with minecraft:netherite_helmet[attribute_modifiers=[],unbreakable={}]
item replace entity @s armor.chest with minecraft:netherite_chestplate[attribute_modifiers=[],unbreakable={}]
item replace entity @s armor.legs with minecraft:netherite_leggings[attribute_modifiers=[],unbreakable={}]
item replace entity @s armor.feet with minecraft:netherite_boots[attribute_modifiers=[],unbreakable={}]
data modify entity @s drop_chances set value {head:0f,chest:0f,legs:0f,feet:0f}

