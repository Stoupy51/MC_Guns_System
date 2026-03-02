
#> mgs:v5.0.0/zombies/bonus/extract_weapon_capacity
#
# @within	mgs:v5.0.0/zombies/bonus/reload_weapon_slot {slot:"$(slot)"}
#
# @args		slot (string)
#

# Copy weapon from player to item_display
$item replace entity @s contents from entity @p[tag=mgs.reloading_weapon] $(slot)

# Read capacity and store as remaining_bullets (refill = set bullets to capacity)
execute store result score #bullets mgs.data run data get entity @s item.components."minecraft:custom_data".mgs.stats.capacity
execute store result storage mgs:temp remaining_bullets int 1 run data get entity @s item.components."minecraft:custom_data".mgs.stats.capacity

# Also store into temp components for lore update
data modify storage mgs:temp components set from entity @s item.components

# Clean up item_display
kill @s

