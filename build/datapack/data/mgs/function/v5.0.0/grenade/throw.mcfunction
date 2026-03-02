
#> mgs:v5.0.0/grenade/throw
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/fire_weapon
#

# Prepare grenade data in storage before summoning
data modify storage mgs:temp grenade set value {}
data modify storage mgs:temp grenade.grenade_type set from storage mgs:gun all.stats.grenade_type
data modify storage mgs:temp grenade.grenade_fuse set from storage mgs:gun all.stats.grenade_fuse
data modify storage mgs:temp grenade.grenade_duration set from storage mgs:gun all.stats.grenade_duration
data modify storage mgs:temp grenade.grenade_effect_radius set from storage mgs:gun all.stats.grenade_effect_radius
data modify storage mgs:temp grenade.expl_damage set from storage mgs:gun all.stats.expl_damage
data modify storage mgs:temp grenade.expl_decay set from storage mgs:gun all.stats.expl_decay
data modify storage mgs:temp grenade.expl_radius set from storage mgs:gun all.stats.expl_radius
data modify storage mgs:temp grenade.proj_gravity set from storage mgs:gun all.stats.proj_gravity
data modify storage mgs:temp grenade.proj_speed set from storage mgs:gun all.stats.proj_speed
data modify storage mgs:temp grenade.proj_model set from storage mgs:gun all.stats.proj_model

# Summon loop (supports pellet_count for multiple grenades)
function mgs:v5.0.0/grenade/summon_loop

# Consume one grenade from the stack (decrease count by 1) - skip if infinite ammo
execute unless score @s mgs.special.infinite_ammo matches 1.. run item modify entity @p[tag=mgs.ticking] weapon.mainhand mgs:v5.0.0/grenade/consume_one

# Set remaining_bullets to 2 so ammo/decrease (which runs after) reduces it to 1 for the next throw
scoreboard players set @s mgs.remaining_bullets 2

