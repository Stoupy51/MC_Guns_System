
#> stoupgun:v5.0.0/ammo/get_current_lore
#
# @within	stoupgun:v5.0.0/ammo/modify_lore {"slot":"$(slot)"}
#

# Copy item lore
$item replace entity @s contents from entity @p[tag=stoupgun.modify_lore] $(slot)
data modify storage stoupgun:temp components set from entity @s item.components
data modify storage stoupgun:temp lore set from storage stoupgun:temp components."minecraft:lore"
data modify storage stoupgun:temp copy set from storage stoupgun:temp lore

# Kill item display
kill @s

