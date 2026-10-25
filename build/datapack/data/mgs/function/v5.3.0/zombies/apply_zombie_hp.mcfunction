
#> mgs:v5.3.0/zombies/apply_zombie_hp
#
# @executed	as @n[tag=mgs.zb_near,sort=random] & at @s
#
# @within	mgs:v5.3.0/zombies/types/normal with storage mgs:temp _zb_hp
#			mgs:v5.3.0/zombies/types/fast with storage mgs:temp _zb_hp
#			mgs:v5.3.0/zombies/types/tank with storage mgs:temp _zb_hp
#			mgs:v5.3.0/zombies/types/armed with storage mgs:temp _zb_hp
#			mgs:v5.3.0/zombies/types/aura with storage mgs:temp _zb_hp
#
# @args		val (unknown)
#

$scoreboard players set @s mgs.zb.max_hp $(val)
$attribute @s minecraft:max_health base set $(val)
execute store result entity @s Health float 1 run attribute @s minecraft:max_health get
function mgs:v5.3.0/zombies/absorb_above_cap

