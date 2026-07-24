
#> mgs:v5.1.0/zombies/perks/deny_requires_power
#
# @executed	as @n[tag=mgs.pk_new]
#
# @within	mgs:v5.1.0/zombies/perks/on_right_click
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.this_perk_machine_requires_power","color":"red"}]
playsound minecraft:entity.villager.no ambient @s ~ ~ ~ 0.8 1.0

