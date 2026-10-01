
#> mgs:v5.1.0/grenade/throw
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/fire_weapon
#			mgs:v5.1.0/mob/fire_weapon
#

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

# Player throws keep the held item's model (camo variants); mobs have no SelectedItem and use the base proj_model.
execute if entity @s[type=player] if data storage mgs:gun SelectedItem.components."minecraft:item_model" run data modify storage mgs:temp grenade.model_override set from storage mgs:gun SelectedItem.components."minecraft:item_model"

# pellet_count gives several grenades.
function mgs:v5.1.0/grenade/summon_loop

# Unless infinite ammo.
execute unless score @s mgs.special.infinite_ammo matches 1.. run item modify entity @p[tag=mgs.ticking] weapon.mainhand mgs:v5.1.0/grenade/consume_one

# ammo/decrease runs next and brings it to 1.
scoreboard players set @s mgs.remaining_bullets 2

