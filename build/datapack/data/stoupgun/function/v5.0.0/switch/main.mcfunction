
#> stoupgun:v5.0.0/switch/main
#
# @within	stoupgun:v5.0.0/player/tick
#

# Set weapon id if not done yet
execute if data storage stoupgun:gun stats unless data storage stoupgun:gun stats.weapon_id run function stoupgun:v5.0.0/switch/set_weapon_id

# If last_selected is different from this one, set cooldown
scoreboard players set #current_id stoupgun.data 0
execute store result score #current_id stoupgun.data run data get storage stoupgun:gun stats.weapon_id
execute unless score @s stoupgun.last_selected = #current_id stoupgun.data store result score @s stoupgun.cooldown run data get storage stoupgun:gun stats.switch

# Update last selected
scoreboard players operation @s stoupgun.last_selected = #current_id stoupgun.data

