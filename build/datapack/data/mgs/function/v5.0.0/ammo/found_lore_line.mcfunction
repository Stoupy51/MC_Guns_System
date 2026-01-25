
#> mgs:v5.0.0/ammo/found_lore_line
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/ammo/search_lore_loop with storage mgs:input with
#
# @args		slot (unknown)
#			index (unknown)
#			capacity (unknown)
#			remaining_bullets (unknown)
#

# Copy item to item display for modification
$item replace entity @s contents from entity @p[tag=mgs.modify_lore] $(slot)

# Update ammo count in lore
$data modify entity @s item.components."minecraft:lore"[$(index)].extra[-1] set value "$(capacity)"
$data modify entity @s item.components."minecraft:lore"[$(index)].extra[-3] set value "$(remaining_bullets)"

# Copy modified item back to player
$item replace entity @p[tag=mgs.modify_lore] $(slot) from entity @s contents

# Clean up item display
kill @s

