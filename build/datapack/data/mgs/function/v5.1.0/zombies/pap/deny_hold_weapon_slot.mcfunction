
#> mgs:v5.1.0/zombies/pap/deny_hold_weapon_slot
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.1.0/zombies/pap/on_right_click
#			mgs:v5.1.0/zombies/pap/upgrade_core
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.hold_weapon_slot_1_2_or_3_to_use_pack_a_punch","color":"red"}]
playsound minecraft:entity.villager.no ambient @s ~ ~ ~ 0.8 1.0

