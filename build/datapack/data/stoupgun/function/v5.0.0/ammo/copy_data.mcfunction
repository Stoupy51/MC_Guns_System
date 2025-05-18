
#> stoupgun:v5.0.0/ammo/copy_data
#
# @within	stoupgun:v5.0.0/switch/on_weapon_switch
#

# Copy the number of remaining bullets
execute store result score @s stoupgun.remaining_bullets run data get storage stoupgun:gun stats.remaining_bullets

# Set remaining bullets to -1 to mark this weapon as needing an update
data modify storage stoupgun:gun stats.remaining_bullets set value -1
item modify entity @s weapon.mainhand stoupgun:v5.0.0/update_stats

