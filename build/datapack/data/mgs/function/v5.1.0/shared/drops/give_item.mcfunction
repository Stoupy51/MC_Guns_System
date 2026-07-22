
#> mgs:v5.1.0/shared/drops/give_item
#
# @executed	at @s
#
# @within	mgs:v5.1.0/shared/drops/give_mag with storage mgs:temp _give [ at @s ]
#
# @args		Item (unknown)
#			Owner (unknown)
#

$summon minecraft:item ~ ~0.2 ~ {Item:$(Item),Owner:$(Owner),PickupDelay:0s,Tags:["mgs.gm_entity"]}

