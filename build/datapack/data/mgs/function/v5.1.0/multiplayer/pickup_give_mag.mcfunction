
#> mgs:v5.1.0/multiplayer/pickup_give_mag
#
# @executed	at @e[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/multiplayer/pickup_collect
#

data modify storage mgs:temp _give set value {}
data modify storage mgs:temp _give.Item set from entity @n[tag=mgs.mp_dropped_gun,distance=..3] item.components."minecraft:custom_data".mgs.drop_mag
data modify storage mgs:temp _give.Owner set from entity @s UUID
execute at @s run function mgs:v5.1.0/multiplayer/pickup_give with storage mgs:temp _give
data remove entity @n[tag=mgs.mp_dropped_gun,distance=..3] item.components."minecraft:custom_data".mgs.drop_mag

