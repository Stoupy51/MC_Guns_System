
#> mgs:v5.4.0/zombies/perks/widows_web_burst
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/grenade/detonate_web with storage mgs:temp _web [ at @s ]
#			mgs:v5.4.0/zombies/perks/widows_on_hurt with storage mgs:temp _web [ at @s ]
#
# @args		radius (unknown)
#

$execute as @e[tag=mgs.zombie_round,distance=..$(radius)] run function mgs:v5.4.0/zombies/perks/widows_web_hit

