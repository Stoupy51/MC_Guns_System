
#> mgs:v5.1.0/switch/force_switch_animation
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/switch/on_weapon_switch
#			mgs:v5.1.0/ammo/reload
#

execute unless data storage mgs:gun all.gun run return fail

# Attack speed follows the cooldown.
function mgs:v5.1.0/switch/sync_attack_speed_with_cooldown

# Swaps when the item matches the previous one (26 chars = "minecraft:poisonous_potato").
execute store result score #current_length mgs.data run data get storage mgs:gun SelectedItem.id
execute if score #current_length mgs.data = @s mgs.previous_selected if score @s mgs.previous_selected matches 26 run item modify entity @s weapon.mainhand {"type": "minecraft:set_item","item": "minecraft:firework_star"}
execute if score #current_length mgs.data = @s mgs.previous_selected unless score @s mgs.previous_selected matches 26 run item modify entity @s weapon.mainhand {"type": "minecraft:set_item","item": "minecraft:poisonous_potato"}

