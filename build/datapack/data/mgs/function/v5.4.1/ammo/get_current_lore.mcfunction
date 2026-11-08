
#> mgs:v5.4.1/ammo/get_current_lore
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/ammo/modify_lore {"slot":"$(slot)"}
#
# @args		slot (string)
#

$item replace entity @s contents from entity @p[tag=mgs.modify_lore] $(slot)

data modify storage mgs:temp components set from entity @s item.components
data modify storage mgs:temp lore set from storage mgs:temp components."minecraft:lore"
data modify storage mgs:temp copy set from storage mgs:temp lore

kill @s

