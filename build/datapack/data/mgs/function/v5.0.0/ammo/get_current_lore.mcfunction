
#> mgs:v5.0.0/ammo/get_current_lore
#
# @within	mgs:v5.0.0/ammo/modify_lore {"slot":"$(slot)"}
#

# Copy weapon to item display entity
$item replace entity @s contents from entity @p[tag=mgs.modify_lore] $(slot)

# Extract lore data
data modify storage mgs:temp components set from entity @s item.components
data modify storage mgs:temp lore set from storage mgs:temp components."minecraft:lore"
data modify storage mgs:temp copy set from storage mgs:temp lore

# Clean up item display
kill @s

