
#> stoupgun:v5.0.0/ammo/modify_lore
#
# @within	stoupgun:v5.0.0/player/right_click {slot:"weapon.mainhand"}
#			stoupgun:v5.0.0/ammo/set_count {slot:"$(slot)"}
#

## In this context, @s has the right amount of bullets in stoupgun.remaining_bullets
# Temporary tag
tag @s add stoupgun.modify_lore

# Copy item lore
$execute summon item_display run function stoupgun:v5.0.0/ammo/get_current_lore {"slot":"$(slot)"}

# Find the ammo line and modify it
scoreboard players set #index stoupgun.data 0
$execute if data storage stoupgun:temp copy[0] run function stoupgun:v5.0.0/ammo/search_lore_loop {"slot":"$(slot)"}

# Remove temporary tag
tag @s remove stoupgun.modify_lore

