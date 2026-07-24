
#> mgs:v5.1.0/zombies/mystery_box/deny_already_in_use
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/mystery_box/box_click
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.mystery_box_is_already_in_use","color":"red"}]
playsound minecraft:entity.villager.no ambient @s ~ ~ ~ 0.8 1.0

