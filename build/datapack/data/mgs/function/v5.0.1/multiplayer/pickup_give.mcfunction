
#> mgs:v5.0.1/multiplayer/pickup_give
#
# @executed	at @p[tag=mgs.mp_drop_picker]
#
# @within	mgs:v5.0.1/multiplayer/pickup_collect with storage mgs:temp _give [ at @p[tag=mgs.mp_drop_picker] ]
#
# @args		Item (unknown)
#			Owner (unknown)
#

$summon minecraft:item ~ ~0.2 ~ {Item:$(Item),Owner:$(Owner),PickupDelay:0s,Tags:["mgs.gm_entity"]}

