
#> mgs:v5.3.0/ammo/get_current_mag_lore
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/ammo/modify_mag_lore {"slot":"$(slot)"}
#
# @args		slot (string)
#

$item replace entity @s contents from entity @p[tag=mgs.modify_mag_lore] $(slot)

data modify storage mgs:temp components set from entity @s item.components
data modify storage mgs:temp lore set from storage mgs:temp components."minecraft:lore"
data modify storage mgs:temp copy set from storage mgs:temp lore

kill @s

