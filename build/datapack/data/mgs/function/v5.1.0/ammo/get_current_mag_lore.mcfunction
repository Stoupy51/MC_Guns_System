
#> mgs:v5.1.0/ammo/get_current_mag_lore
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/ammo/modify_mag_lore {"slot":"$(slot)"}
#
# @args		slot (string)
#

$item replace entity @s contents from entity @p[tag=mgs.modify_mag_lore] $(slot)

data modify storage mgs:temp components set from entity @s item.components
data modify storage mgs:temp lore set from storage mgs:temp components."minecraft:lore"
data modify storage mgs:temp copy set from storage mgs:temp lore

kill @s

