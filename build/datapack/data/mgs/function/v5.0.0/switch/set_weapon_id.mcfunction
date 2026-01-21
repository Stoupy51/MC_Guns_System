
#> mgs:v5.0.0/switch/set_weapon_id
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/switch/main
#

execute store result storage mgs:gun all.stats.weapon_id int 1 run scoreboard players add #next_id mgs.data 1

# Initialize fire mode to 'auto' if weapon supports it, otherwise 'semi'
execute unless data storage mgs:gun all.stats.fire_mode if data storage mgs:gun all.stats.can_auto run data modify storage mgs:gun all.stats.fire_mode set value "auto"
execute unless data storage mgs:gun all.stats.fire_mode unless data storage mgs:gun all.stats.can_auto run data modify storage mgs:gun all.stats.fire_mode set value "semi"

item modify entity @s weapon.mainhand mgs:v5.0.0/set_weapon_id

