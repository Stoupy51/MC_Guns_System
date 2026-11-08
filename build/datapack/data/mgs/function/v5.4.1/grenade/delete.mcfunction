
#> mgs:v5.4.1/grenade/delete
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/grenade/detonate_web
#			mgs:v5.4.1/grenade/detonate_frag
#			mgs:v5.4.1/grenade/detonate_flash
#			mgs:v5.4.1/grenade/tick_effect
#

execute if entity @s[tag=mgs.stuck_to_entity] run function mgs:v5.4.1/grenade/cleanup_stuck_entity

kill @s

