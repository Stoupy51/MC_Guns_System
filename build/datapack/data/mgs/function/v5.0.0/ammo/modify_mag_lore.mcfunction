
#> mgs:v5.0.0/ammo/modify_mag_lore
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/ammo/inventory/process_slot {slot:"$(slot)"}
#
# @args		slot (string)
#

# Add temporary tag for item display targeting
tag @s add mgs.modify_mag_lore

# Get current item lore
$execute summon item_display run function mgs:v5.0.0/ammo/get_current_mag_lore {"slot":"$(slot)"}

# Find and update ammo count in lore
scoreboard players set #index mgs.data 0
$execute if data storage mgs:temp copy[0] run function mgs:v5.0.0/ammo/search_mag_lore_loop {"slot":"$(slot)"}

# Clean up temporary tag
tag @s remove mgs.modify_mag_lore

