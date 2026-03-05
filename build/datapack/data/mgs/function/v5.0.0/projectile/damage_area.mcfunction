
#> mgs:v5.0.0/projectile/damage_area
#
# @executed	at @s
#
# @within	mgs:v5.0.0/projectile/explode with storage mgs:temp expl
#			mgs:v5.0.0/grenade/detonate_frag with storage mgs:temp expl
#
# @args		radius_float (unknown)
#

$execute as @e[type=!#bs.hitbox:intangible,distance=..$(radius_float)] run function mgs:v5.0.0/projectile/damage_entity

