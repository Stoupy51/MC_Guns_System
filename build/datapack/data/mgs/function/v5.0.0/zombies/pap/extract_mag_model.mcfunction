
#> mgs:v5.0.0/zombies/pap/extract_mag_model
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/upgrade_magazine_slot {slot:"$(slot)"}
#
# @args		slot (string)
#

$item replace entity @s contents from entity @p[tag=mgs.pap_extracting_mag] $(slot)
data modify storage mgs:temp refill.mag_model set from entity @s item.components."minecraft:item_model"
kill @s

