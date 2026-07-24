
#> mgs:v5.1.0/zombies/wallbuys/deny_hold_valid_slot
#
# @within	mgs:v5.1.0/zombies/wallbuys/replace_selected
#

execute if score @s mgs.zb.perk.mule_kick matches 1.. run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.hold_weapon_slot_1_2_or_3_to_swap_your_current_gun","color":"red"}]
execute unless score @s mgs.zb.perk.mule_kick matches 1.. run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.hold_weapon_slot_1_or_2_to_swap_your_current_gun","color":"red"}]
playsound minecraft:entity.villager.no ambient @s ~ ~ ~ 0.8 1.0

