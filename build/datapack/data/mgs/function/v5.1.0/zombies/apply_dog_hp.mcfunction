
#> mgs:v5.1.0/zombies/apply_dog_hp
#
# @executed	as @e[tag=...]
#
# @within	mgs:v5.1.0/zombies/types/dog with storage mgs:temp _zb_hp
#
# @args		val (unknown)
#

$attribute @s minecraft:max_health modifier add mgs:dog_hp $(val) add_value
execute store result entity @s Health float 1 run attribute @s minecraft:max_health get

