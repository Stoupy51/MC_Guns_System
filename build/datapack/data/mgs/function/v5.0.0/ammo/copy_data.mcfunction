
#> mgs:v5.0.0/ammo/copy_data
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/switch/on_weapon_switch
#

# Load ammo count from weapon into player's scoreboard (if different from -1)
execute store result score #count mgs.data run data get storage mgs:gun all.stats.remaining_bullets
execute unless score #count mgs.data matches -1 run scoreboard players operation @s mgs.remaining_bullets = #count mgs.data

# Mark weapon as needing update
data modify storage mgs:gun all.stats.remaining_bullets set value -1
item modify entity @s weapon.mainhand mgs:v5.0.0/update_stats

