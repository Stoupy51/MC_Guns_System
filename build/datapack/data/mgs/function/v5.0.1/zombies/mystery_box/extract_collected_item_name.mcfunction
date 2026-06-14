
#> mgs:v5.0.1/zombies/mystery_box/extract_collected_item_name
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.0.1/zombies/mystery_box/capture_collected_name_slot {slot:"$(slot)"}
#
# @args		slot (string)
#

$item replace entity @s contents from entity @p[tag=mgs.mb_name_reader] $(slot)
data modify storage mgs:temp _mb_collected_name set from entity @s item.components."minecraft:item_name"
kill @s

