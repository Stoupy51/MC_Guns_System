
#> mgs:v5.1.0/grenade/delete
#
# @executed	at @s
#
# @within	mgs:v5.1.0/grenade/detonate_web
#			mgs:v5.1.0/grenade/detonate_frag
#			mgs:v5.1.0/grenade/detonate_flash
#			mgs:v5.1.0/grenade/tick_effect
#

execute if entity @s[tag=mgs.stuck_to_entity] run function mgs:v5.1.0/grenade/cleanup_stuck_entity

kill @s

