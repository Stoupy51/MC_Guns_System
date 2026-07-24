
#> mgs:v5.1.0/shared/drops/overkill_check
#
# @executed	at @e[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/shared/drops/collect
#

# Only primary drops are restricted
data modify storage mgs:temp _isp set value {}
data modify storage mgs:temp _isp.bw set from entity @n[type=minecraft:item_display,tag=mgs.dropped_gun,distance=..3] item.components."minecraft:custom_data".mgs.stats.base_weapon
function mgs:v5.1.0/shared/drops/is_primary_lookup
execute if score #is_primary mgs.data matches 0 run return 0

# Overkill lets you carry two primary weapons
scoreboard players add @s mgs.special.overkill 0
execute if score @s mgs.special.overkill matches 1.. run return 0

# The slot that keeps its gun after this pickup: the held slot when taking, the other slot when swapping
scoreboard players operation #pick_keep mgs.data = #pick_sel mgs.data
execute if score #pick_g0 mgs.data matches 1 if score #pick_g1 mgs.data matches 1 run scoreboard players set #pick_keep mgs.data 1
execute if score #pick_g0 mgs.data matches 1 if score #pick_g1 mgs.data matches 1 run scoreboard players operation #pick_keep mgs.data -= #pick_sel mgs.data

# If the kept gun is also a primary, deny the pickup
data modify storage mgs:temp _isp set value {}
execute if score #pick_keep mgs.data matches 0 run data modify storage mgs:temp _isp.bw set from entity @s Inventory[{Slot:0b}].components."minecraft:custom_data".mgs.stats.base_weapon
execute if score #pick_keep mgs.data matches 1 run data modify storage mgs:temp _isp.bw set from entity @s Inventory[{Slot:1b}].components."minecraft:custom_data".mgs.stats.base_weapon
function mgs:v5.1.0/shared/drops/is_primary_lookup
execute if score #is_primary mgs.data matches 0 run return 0

scoreboard players set #pick_deny mgs.data 1
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.you_need_the_overkill_perk_to_carry_two_primary_weapons","color":"red"}]
playsound minecraft:entity.villager.no ambient @s ~ ~ ~ 0.8 1.0

