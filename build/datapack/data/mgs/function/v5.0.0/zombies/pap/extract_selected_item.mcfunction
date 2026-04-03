
#> mgs:v5.0.0/zombies/pap/extract_selected_item
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/extract_selected {slot:"$(slot)"}
#
# @args		slot (string)
#

$item replace entity @s contents from entity @p[tag=mgs.pap_extracting] $(slot)

data modify storage mgs:temp _pap_extract set value {}
data modify storage mgs:temp _pap_extract.weapon set from entity @s item.components."minecraft:custom_data".mgs.weapon
data modify storage mgs:temp _pap_extract.stats set from entity @s item.components."minecraft:custom_data".mgs.stats
execute if data entity @s item.components."minecraft:item_name"[0].text run data modify storage mgs:temp _pap_extract.current_name set from entity @s item.components."minecraft:item_name"[0].text
execute if data entity @s item.components."minecraft:lore"[0] run data modify storage mgs:temp _pap_extract.lore set from entity @s item.components."minecraft:lore"
kill @s

