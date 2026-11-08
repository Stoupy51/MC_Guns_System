
#> mgs:v5.4.1/zombies/bonus/extract_weapon_capacity
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/bonus/reload_weapon_slot {slot:"$(slot)"}
#
# @args		slot (string)
#

$item replace entity @s contents from entity @p[tag=mgs.reloading_weapon] $(slot)

execute store result score #bullets mgs.data run data get entity @s item.components."minecraft:custom_data".mgs.stats.capacity
execute store result storage mgs:temp remaining_bullets int 1 run data get entity @s item.components."minecraft:custom_data".mgs.stats.capacity

data modify storage mgs:temp components set from entity @s item.components

kill @s

