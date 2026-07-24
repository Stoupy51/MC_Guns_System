
#> mgs:v5.1.0/zombies/mystery_box/deny_moving
#
# @executed	as @n[tag=mgs.mb_new]
#
# @within	mgs:v5.1.0/zombies/mystery_box/on_right_click
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.the_mystery_box_is_moving","color":"yellow"}]
playsound minecraft:entity.villager.no ambient @s ~ ~ ~ 0.8 1.0

