
#> mgs:v5.3.0/zombies/apply_zombie_absorption
#
# @executed	as @n[tag=mgs.zb_near,sort=random] & at @s
#
# @within	mgs:v5.3.0/zombies/absorb_above_cap with storage mgs:temp _zb_absorb
#
# @args		val (unknown)
#

$attribute @s minecraft:max_absorption base set $(val)
$data modify entity @s AbsorptionAmount set value $(val)f

