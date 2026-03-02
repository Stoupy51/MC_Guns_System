
#> mgs:v5.0.0/grenade/delete
#
# @executed	as @e[tag=mgs.grenade] & at @s
#
# @within	mgs:v5.0.0/grenade/detonate_frag
#			mgs:v5.0.0/grenade/detonate_flash
#			mgs:v5.0.0/grenade/tick_effect
#

# If stuck to an entity, clean up the target's stuck_id
execute if entity @s[tag=mgs.stuck_to_entity] run function mgs:v5.0.0/grenade/cleanup_stuck_entity

# Decrease grenade counter and kill entity
scoreboard players remove #grenade_count mgs.data 1
kill @s

