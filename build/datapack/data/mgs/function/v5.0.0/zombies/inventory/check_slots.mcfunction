
#> mgs:v5.0.0/zombies/inventory/check_slots
#
# @executed	as the player & at current position
#
# @within	mgs:v5.0.0/zombies/inventory/on_change
#

# Knife must be in hotbar.0
execute unless items entity @s hotbar.0 minecraft:iron_sword[custom_data~{mgs:{knife:true}}] run function mgs:v5.0.0/zombies/inventory/fix_knife

# Info item must be in hotbar.8
execute unless items entity @s hotbar.8 *[custom_data~{mgs:{zb_info:true}}] run function mgs:v5.0.0/zombies/inventory/fix_info

# Grenade must be in hotbar.7
execute unless items entity @s hotbar.7 *[custom_data~{mgs:{gun:true,stats:{grenade_type:"frag"}}}] run function mgs:v5.0.0/zombies/inventory/fix_grenade

# Ability item must be in hotbar.4 (if player has ability)
execute if score @s mgs.zb.ability matches 1.. unless items entity @s hotbar.4 *[custom_data~{mgs:{zb_ability_item:true}}] run function mgs:v5.0.0/zombies/inventory/give_ability_item

# Weapon in hotbar.1 must be a gun
execute unless items entity @s hotbar.1 *[custom_data~{mgs:{gun:true}}] run function mgs:v5.0.0/zombies/inventory/fix_weapon_1

# Magazine in inventory.1 should exist if weapon 1 exists
execute if items entity @s hotbar.1 *[custom_data~{mgs:{gun:true}}] unless items entity @s inventory.1 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/inventory/fix_mag_1

# Prevent items in forbidden slots
item replace entity @s hotbar.5 with air

# Clear cursor (prevent holding mgs items outside inventory)
execute if items entity @s player.cursor *[custom_data~{mgs:}] run item replace entity @s player.cursor with air

