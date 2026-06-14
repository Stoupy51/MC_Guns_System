
#> mgs:v5.0.1/multiplayer/pickup_collect
#
# @executed	at @e[tag=bs.interaction.target]
#
# @within	mgs:v5.0.1/multiplayer/pickup_dropped_weapon [ at @e[tag=bs.interaction.target] ]
#

execute unless entity @n[tag=mgs.mp_dropped_gun,distance=..3] run return fail
data modify storage mgs:temp _give set value {}
data modify storage mgs:temp _give.Item set from entity @n[tag=mgs.mp_dropped_gun,distance=..3] item
data modify storage mgs:temp _give.Owner set from entity @p[tag=mgs.mp_drop_picker] UUID
execute at @p[tag=mgs.mp_drop_picker] run function mgs:v5.0.1/multiplayer/pickup_give with storage mgs:temp _give
kill @n[tag=mgs.mp_dropped_gun,distance=..3]
kill @e[tag=bs.interaction.target]

