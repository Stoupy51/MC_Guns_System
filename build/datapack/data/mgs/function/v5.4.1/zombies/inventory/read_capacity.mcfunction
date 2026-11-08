
#> mgs:v5.4.1/zombies/inventory/read_capacity
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/inventory/scale_magazine_slot {slot:"hotbar.$(index)",multiplier:6}
#
# @args		slot (string)
#			multiplier (int)
#

$item replace entity @s contents from entity @p[tag=mgs.zb_scaling_mag] $(slot)
$execute store result score #zb_cap mgs.data run data get entity @s item.components."minecraft:custom_data".mgs.stats.capacity $(multiplier)
kill @s

