
#> mgs:v5.4.0/zombies/pap/extract_mag_model
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/pap/upgrade_magazine_slot {slot:"$(slot)"}
#
# @args		slot (string)
#

$item replace entity @s contents from entity @p[tag=mgs.pap_extracting_mag] $(slot)
data modify storage mgs:temp refill.mag_model set from entity @s item.components."minecraft:item_model"
kill @s

