
#> mgs:v5.1.0/ammo/copy_data
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/switch/on_weapon_switch
#

# Unless it is already -1.
execute store result score #count mgs.data run data get storage mgs:gun all.stats.remaining_bullets
execute unless score #count mgs.data matches -1 run scoreboard players operation @s mgs.remaining_bullets = #count mgs.data

data modify storage mgs:gun all.stats.remaining_bullets set value -1
item modify entity @s weapon.mainhand mgs:v5.1.0/update_stats

