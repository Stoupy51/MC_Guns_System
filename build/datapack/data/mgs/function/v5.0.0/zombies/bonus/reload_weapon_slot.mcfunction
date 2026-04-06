
#> mgs:v5.0.0/zombies/bonus/reload_weapon_slot
#
# @within	mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"hotbar.0"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"hotbar.1"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"hotbar.2"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"hotbar.3"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"hotbar.4"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"hotbar.5"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"hotbar.6"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"hotbar.7"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"hotbar.8"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"weapon.offhand"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.0"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.1"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.2"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.3"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.4"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.5"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.6"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.7"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.8"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.9"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.10"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.11"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.12"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.13"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.14"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.15"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.16"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.17"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.18"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.19"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.20"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.21"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.22"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.23"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.24"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.25"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.26"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"player.cursor"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"player.crafting.0"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"player.crafting.1"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"player.crafting.2"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons {slot:"player.crafting.3"}
#			mgs:v5.0.0/zombies/pap/apply_to_slot {slot:"$(slot)"}
#			mgs:v5.0.0/zombies/wallbuys/give_to_slot {slot:"hotbar.$(hotbar)"}
#			mgs:v5.0.0/zombies/wallbuys/reload_pair {slot:"hotbar.$(hotbar)"}
#			mgs:v5.0.0/zombies/wallbuys/replace_pair {slot:"hotbar.$(hotbar)"}
#
# @args		slot (string)
#

# Extract weapon capacity and set remaining_bullets = capacity
tag @s add mgs.reloading_weapon
$execute summon item_display run function mgs:v5.0.0/zombies/bonus/extract_weapon_capacity {slot:"$(slot)"}
tag @s remove mgs.reloading_weapon

# Save current ammo display (so non-active slot reloads don't corrupt the active HUD)
scoreboard players operation #rws_save mgs.data = @s mgs.remaining_bullets

# Set player scoreboard to capacity (needed by modify_lore)
scoreboard players operation @s mgs.remaining_bullets = #bullets mgs.data

# If this is the active mainhand weapon (remaining_bullets = -1 sentinel), only update lore
# (don't write CAPACITY to item NBT - the player's scoreboard is the source of truth)
$execute if items entity @s $(slot) *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/modify_lore {slot:"$(slot)"}

# For slots with inactive weapons: write CAPACITY to item NBT
$item modify entity @s $(slot) mgs:v5.0.0/update_ammo

# Update weapon lore
$function mgs:v5.0.0/ammo/modify_lore {slot:"$(slot)"}

# Restore the active weapon's ammo display for non-active slots
scoreboard players operation @s mgs.remaining_bullets = #rws_save mgs.data

