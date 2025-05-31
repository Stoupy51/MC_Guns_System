
#> mgs:v5.0.0/ammo/found_line
#
# @within	mgs:v5.0.0/ammo/search_lore_loop with storage mgs:input with
#

# Copy weapon to item display for modification
$item replace entity @s contents from entity @p[tag=mgs.modify_lore] $(slot)

# Update ammo count in lore
$data modify entity @s item.components."minecraft:lore"[$(index)].extra[-1] set value "$(capacity)"
$data modify entity @s item.components."minecraft:lore"[$(index)].extra[-3] set value "$(remaining_bullets)"

# Copy modified weapon back to player
$item replace entity @p[tag=mgs.modify_lore] $(slot) from entity @s contents

# Clean up item display
kill @s

