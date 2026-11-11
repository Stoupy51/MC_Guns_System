
#> mgs:v5.4.2/ammo/copy_data
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/switch/on_weapon_switch
#

# Unless it is already -1.
execute store result score #count mgs.data run data get storage mgs:gun all.stats.remaining_bullets
execute unless score #count mgs.data matches -1 run scoreboard players operation @s mgs.remaining_bullets = #count mgs.data

data modify storage mgs:gun all.stats.remaining_bullets set value -1
item modify entity @s weapon.mainhand mgs:v5.4.2/update_stats

