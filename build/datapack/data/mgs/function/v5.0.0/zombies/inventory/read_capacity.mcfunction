
#> mgs:v5.0.0/zombies/inventory/read_capacity
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/inventory/scale_magazine_slot {slot:"hotbar.$(index)",multiplier:6}
#
# @args		slot (string)
#			multiplier (int)
#

$item replace entity @s contents from entity @p[tag=mgs.zb_scaling_mag] $(slot)
$execute store result score #zb_cap mgs.data run data get entity @s item.components."minecraft:custom_data".mgs.stats.capacity $(multiplier)
kill @s

