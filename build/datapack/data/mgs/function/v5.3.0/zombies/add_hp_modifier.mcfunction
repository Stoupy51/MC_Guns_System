
#> mgs:v5.3.0/zombies/add_hp_modifier
#
# @executed	as @n[tag=mgs.zb_new]
#
# @within	mgs:v5.3.0/zombies/apply_zombie_hp with storage mgs:temp _zb_hp
#
# @args		val (unknown)
#

$attribute @s minecraft:max_health modifier add mgs:round_hp $(val) add_value

