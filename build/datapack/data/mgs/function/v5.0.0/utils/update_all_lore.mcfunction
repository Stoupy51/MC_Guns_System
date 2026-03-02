
#> mgs:v5.0.0/utils/update_all_lore
#
# @within	mgs:v5.0.0/utils/update_all_lore {slot:"weapon.mainhand"}
#
# @args		slot (string)
#

# Rebuild all lore lines for the weapon in the given slot from its current stats
# Usage: function mgs:v5.0.0/utils/update_all_lore {slot:"weapon.mainhand"}

# Tag player for identification
tag @s add mgs.update_lore

# Read stats from item into scores
$execute summon item_display run function mgs:v5.0.0/lore/extract_stats {"slot":"$(slot)"}

# Skip if not a gun
execute if score #is_gun mgs.data matches 0 run return run tag @s remove mgs.update_lore

# Compute formatted display values (integer math → storage for macros)
function mgs:v5.0.0/lore/compute_values

# Build new lore based on weapon type
execute if score #is_grenade mgs.data matches 1 run function mgs:v5.0.0/lore/build_grenade with storage mgs:input lore
execute if score #is_grenade mgs.data matches 0 run function mgs:v5.0.0/lore/build_gun with storage mgs:input lore

# Restore footer (branding line saved during extraction)
data modify storage mgs:temp new_lore append from storage mgs:temp lore_footer

# Apply new lore to item
$execute summon item_display run function mgs:v5.0.0/lore/apply {"slot":"$(slot)"}

# Clean up
tag @s remove mgs.update_lore

