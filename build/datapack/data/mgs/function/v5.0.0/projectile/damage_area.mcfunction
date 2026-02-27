
#> mgs:v5.0.0/projectile/damage_area
#
# @executed	as @e[tag=mgs.slow_bullet] & at @s
#
# @within	mgs:v5.0.0/projectile/explode with storage mgs:temp expl
#
# @args		radius_int (unknown)
#

$execute as @e[type=!#bs.hitbox:intangible,distance=..$(radius_int)] run function mgs:v5.0.0/projectile/damage_entity

