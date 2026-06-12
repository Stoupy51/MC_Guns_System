
#> mgs:v5.0.1/ammo/modify_lore
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/right_click {slot:"weapon.mainhand"}
#			mgs:v5.0.1/zoom/remove {slot:"weapon.mainhand"}
#			mgs:v5.0.1/zoom/set {slot:"weapon.mainhand"}
#			mgs:v5.0.1/ammo/set_count {slot:"$(slot)"}
#			mgs:v5.0.1/ammo/end_reload {slot:"weapon.mainhand"}
#			mgs:v5.0.1/zombies/bonus/reload_weapon_slot {slot:"$(slot)"}
#
# @args		slot (string)
#

# Add temporary tag for item display targeting
tag @s add mgs.modify_lore

# Get current item lore
$execute summon item_display run function mgs:v5.0.1/ammo/get_current_lore {"slot":"$(slot)"}

# Find and update ammo count in lore
scoreboard players set #index mgs.data 0
$execute if data storage mgs:temp copy[0] run function mgs:v5.0.1/ammo/search_lore_loop {"slot":"$(slot)"}

# Clean up temporary tag
tag @s remove mgs.modify_lore

