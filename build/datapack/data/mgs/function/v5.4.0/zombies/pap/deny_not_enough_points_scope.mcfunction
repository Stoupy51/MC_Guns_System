
#> mgs:v5.4.0/zombies/pap/deny_not_enough_points_scope
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/pap/repap_scope_only
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.you_dont_have_enough_points_1000_needed","fallback":"You don't have enough points (1000 needed).","color":"red"}]
playsound minecraft:entity.villager.no ambient @s ~ ~ ~ 0.8 1.0

