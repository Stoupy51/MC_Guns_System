
#> mgs:v5.4.3/projectile/damage_area
#
# @within	mgs:v5.4.3/dialog/close_then
#			mgs:v5.4.3/projectile/explode with storage mgs:temp expl
#			mgs:v5.4.3/grenade/detonate_frag with storage mgs:temp expl
#
# @args		radius_float (unknown)
#

$execute as @e[type=!#mgs:ignore,distance=..$(radius_float),tag=!global.ignore.kill,tag=!global.ignore,nbt=!{Invulnerable:true}] run function mgs:v5.4.3/projectile/damage_entity

