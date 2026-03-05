
#> mgs:v5.0.0/grenade/flash_apply
#
# @executed	as @e[tag=mgs.grenade] & at @s
#
# @within	mgs:v5.0.0/grenade/detonate_flash
#

# Apply blindness and darkness effects to all players within radius
execute store result storage mgs:temp flash.radius_float float 1 run data get entity @s data.config.grenade_effect_radius
function mgs:v5.0.0/grenade/flash_area with storage mgs:temp flash

