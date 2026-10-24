
#> mgs:v5.2.0/zombies/pap/deny_not_enough_points_scope
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.2.0/zombies/pap/repap_scope_only
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.you_dont_have_enough_points_1000_needed","fallback":"You don't have enough points (1000 needed).","color":"red"}]
playsound minecraft:entity.villager.no ambient @s ~ ~ ~ 0.8 1.0

