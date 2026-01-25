
#> mgs:v5.0.0/ammo/modify_lore
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/right_click {slot:"weapon.mainhand"}
#			mgs:v5.0.0/zoom/remove {slot:"weapon.mainhand"}
#			mgs:v5.0.0/zoom/set {slot:"weapon.mainhand"}
#			mgs:v5.0.0/ammo/set_count {slot:"$(slot)"}
#			mgs:v5.0.0/ammo/reload {slot:"weapon.mainhand"}
#			mgs:v5.0.0/ammo/end_reload {slot:"weapon.mainhand"}
#
# @args		slot (string)
#

# Add temporary tag for item display targeting
tag @s add mgs.modify_lore

# Get current item lore
$execute summon item_display run function mgs:v5.0.0/ammo/get_current_lore {"slot":"$(slot)"}

# Find and update ammo count in lore
scoreboard players set #index mgs.data 0
$execute if data storage mgs:temp copy[0] run function mgs:v5.0.0/ammo/search_lore_loop {"slot":"$(slot)"}

# Clean up temporary tag
tag @s remove mgs.modify_lore

## In this context, @s has the right amount of bullets in mgs.remaining_bullets
# Add temporary tag for item display targeting
tag @s add mgs.modify_lore

# Get current weapon lore
$execute summon item_display run function mgs:v5.0.0/ammo/get_current_lore {"slot":"$(slot)"}

# Find and update ammo count in lore
scoreboard players set #index mgs.data 0
$execute if data storage mgs:temp copy[0] run function mgs:v5.0.0/ammo/search_lore_loop {"slot":"$(slot)"}

# Clean up temporary tag
tag @s remove mgs.modify_lore

