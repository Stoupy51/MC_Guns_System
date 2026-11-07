
#> mgs:v5.4.0/zombies/add_hp_modifier
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/apply_zombie_hp with storage mgs:temp _zb_hp
#
# @args		val (unknown)
#

$attribute @s minecraft:max_health modifier add mgs:round_hp $(val) add_value

