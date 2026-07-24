
#> mgs:v5.1.0/zombies/mystery_box/deny_all_owned
#
# @executed	as @a[scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.1.0/zombies/mystery_box/result_all_owned [ as @a[scores={mgs.zb.in_game=1}] ]
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.you_already_own_all_available_mystery_box_weapons_points_refunde","color":"yellow"}]
playsound minecraft:entity.villager.no ambient @s ~ ~ ~ 0.8 1.0

