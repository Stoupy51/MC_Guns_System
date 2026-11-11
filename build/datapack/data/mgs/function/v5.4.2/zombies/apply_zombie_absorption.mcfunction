
#> mgs:v5.4.2/zombies/apply_zombie_absorption
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/absorb_above_cap with storage mgs:temp _zb_absorb
#
# @args		val (unknown)
#

$attribute @s minecraft:max_absorption base set $(val)
$data modify entity @s AbsorptionAmount set value $(val)f

