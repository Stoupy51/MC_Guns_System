
#> stoupgun:v5.0.0/ammo/copy_data
#
# @within	stoupgun:v5.0.0/switch/on_weapon_switch
#

# Load ammo count from weapon into player's scoreboard (if different from -1)
execute store result score #count stoupgun.data run data get storage stoupgun:gun all.stats.remaining_bullets
execute unless score #count stoupgun.data matches -1 run scoreboard players operation @s stoupgun.remaining_bullets = #count stoupgun.data

# Mark weapon as needing update
data modify storage stoupgun:gun all.stats.remaining_bullets set value -1
item modify entity @s weapon.mainhand stoupgun:v5.0.0/update_stats

