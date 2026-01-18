
#> mgs:v5.0.0/switch/force_switch_animation
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/switch/on_weapon_switch
#			mgs:v5.0.0/ammo/reload
#

# Stop if no weapon in hand
execute unless data storage mgs:gun all.stats run return fail

# Modify attack_speed attribute modifier to sync with current cooldown
function mgs:v5.0.0/switch/sync_attack_speed_with_cooldown

# Swap weapon in hand if same as previously selected (27 = length of string 'minecraft:carrot_on_a_stick')
execute store result score #current_length mgs.data run data get storage mgs:gun SelectedItem.id
execute if score #current_length mgs.data = @s mgs.previous_selected if score @s mgs.previous_selected matches 27 run item modify entity @s weapon.mainhand {"function": "minecraft:set_item","item": "minecraft:warped_fungus_on_a_stick"}
execute if score #current_length mgs.data = @s mgs.previous_selected unless score @s mgs.previous_selected matches 27 run item modify entity @s weapon.mainhand {"function": "minecraft:set_item","item": "minecraft:carrot_on_a_stick"}

