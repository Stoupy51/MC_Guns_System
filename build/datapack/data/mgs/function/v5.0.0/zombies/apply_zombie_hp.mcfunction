
#> mgs:v5.0.0/zombies/apply_zombie_hp
#
# @within	mgs:v5.0.0/zombies/types/normal with storage mgs:temp _zb_hp
#
# @args		val (unknown)
#

$attribute @s minecraft:max_health base set $(val)
execute store result entity @s Health float 1 run attribute @s minecraft:max_health get

