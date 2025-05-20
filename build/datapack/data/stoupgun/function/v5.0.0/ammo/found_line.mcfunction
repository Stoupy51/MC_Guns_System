
#> stoupgun:v5.0.0/ammo/found_line
#
# @within	stoupgun:v5.0.0/ammo/search_lore_loop with storage stoupgun:input with
#

# Copy item to the item display
$item replace entity @s contents from entity @p[tag=stoupgun.modify_lore] $(slot)

# Modify lore
$data modify entity @s item.components."minecraft:lore"[$(index)].extra[-1] set value "$(capacity)"
$data modify entity @s item.components."minecraft:lore"[$(index)].extra[-3] set value "$(remaining_bullets)"

# Copy back the item to the player
$item replace entity @p[tag=stoupgun.modify_lore] $(slot) from entity @s contents

# Kill item display
kill @s

