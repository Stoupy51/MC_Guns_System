
#> stoupgun:v5.0.0/ammo/modify_lore
#
# @within	stoupgun:v5.0.0/player/right_click {slot:"weapon.mainhand"}
#			stoupgun:v5.0.0/zoom/remove {slot:"weapon.mainhand"}
#			stoupgun:v5.0.0/zoom/set {slot:"weapon.mainhand"}
#			stoupgun:v5.0.0/ammo/set_count {slot:"$(slot)"}
#

## In this context, @s has the right amount of bullets in stoupgun.remaining_bullets
# Add temporary tag for item display targeting
tag @s add stoupgun.modify_lore

# Get current weapon lore
$execute summon item_display run function stoupgun:v5.0.0/ammo/get_current_lore {"slot":"$(slot)"}

# Find and update ammo count in lore
scoreboard players set #index stoupgun.data 0
$execute if data storage stoupgun:temp copy[0] run function stoupgun:v5.0.0/ammo/search_lore_loop {"slot":"$(slot)"}

# Clean up temporary tag
tag @s remove stoupgun.modify_lore

