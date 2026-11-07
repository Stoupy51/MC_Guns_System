
#> mgs:v5.4.0/shared/drops/give_item
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/shared/drops/give_mag with storage mgs:temp _give [ at @s ]
#
# @args		Item (unknown)
#			Owner (unknown)
#

$summon minecraft:item ~ ~0.2 ~ {Item:$(Item),Owner:$(Owner),PickupDelay:0s}

