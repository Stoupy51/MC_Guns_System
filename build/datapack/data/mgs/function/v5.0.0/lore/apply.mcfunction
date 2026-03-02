
#> mgs:v5.0.0/lore/apply
#
# @within	mgs:v5.0.0/utils/update_all_lore {"slot":"$(slot)"}
#
# @args		slot (string)
#

# Copy item from player to item_display
$item replace entity @s contents from entity @p[tag=mgs.update_lore] $(slot)

# Replace lore with rebuilt version
data modify entity @s item.components."minecraft:lore" set from storage mgs:temp new_lore

# Copy modified item back to player
$item replace entity @p[tag=mgs.update_lore] $(slot) from entity @s contents

# Clean up
kill @s

