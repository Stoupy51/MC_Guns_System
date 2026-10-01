
#> mgs:v5.1.0/zombies/mystery_box/deny_pool_empty
#
# @within	mgs:v5.1.0/zombies/mystery_box/pick_random_result
#

# A stale result would make the pull look successful.
data remove storage mgs:zombies mystery_box.result
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.the_mystery_box_has_no_weapons_available","color":"red"}]
playsound minecraft:entity.villager.no ambient @s ~ ~ ~ 0.8 1.0

